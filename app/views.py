from datetime import date, datetime, timedelta

import phonenumbers as ph
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Count, Min, Q
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from phonenumbers import NumberParseException

from .forms import OrderForm
from .models import FAQ, Box, CategoryFAQ, Client, Order, Warehouse


def index(request):
    return render(request, "index.html")


def faq(request):
    categories = CategoryFAQ.objects.all()
    faq = []
    for category in categories:
        faq.append({category.name: FAQ.objects.filter(category=category)})
    context = {"categories": categories, "faq": faq}
    return render(request, "faq.html", context)


def boxes(request):
    warehouses = Warehouse.objects.annotate(
        total_boxes=Count("box"),
        free_boxes=Count("box", filter=Q(box__is_occupied=False)),
        min_price_box=Min("box__price"),
    )
    first_warehouse = warehouses.first()
    boxes = Box.objects.filter(storage=first_warehouse, is_occupied=False)
    boxes_to3 = boxes.filter(volume__gt=0, volume__lt=3, is_occupied=False)
    boxes_to10 = boxes.filter(volume__gte=3, volume__lt=10, is_occupied=False)
    boxes_from10 = boxes.filter(volume__gte=10, is_occupied=False)
    form = OrderForm(user=request.user)
    context = {
        "warehouses": warehouses,
        "boxes": boxes,
        "boxes_to3": boxes_to3,
        "boxes_to10": boxes_to10,
        "boxes_from10": boxes_from10,
        "form": form,
    }
    return render(request, "boxes.html", context)


def filter_boxes(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)
    boxes = Box.objects.filter(storage=warehouse, is_occupied=False)
    boxes_to3 = boxes.filter(volume__gt=0, volume__lt=3, is_occupied=False)
    boxes_to10 = boxes.filter(volume__gte=3, volume__lt=10, is_occupied=False)
    boxes_from10 = boxes.filter(volume__gte=10, is_occupied=False)
    boxes_html = render_to_string("boxes_partial.html", {"boxes": boxes})
    boxes_to3_html = render_to_string(
        "boxes_partial.html", {"boxes": boxes_to3}
    )
    boxes_to10_html = render_to_string(
        "boxes_partial.html", {"boxes": boxes_to10}
    )
    boxes_from10_html = render_to_string(
        "boxes_partial.html", {"boxes": boxes_from10}
    )

    return JsonResponse(
        {
            "boxes_html": boxes_html,
            "boxes_to3_html": boxes_to3_html,
            "boxes_to10_html": boxes_to10_html,
            "boxes_from10_html": boxes_from10_html,
        }
    )


def create_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Заказ успешно создан! Проверьте почту.",
                }
            )
        else:
            return JsonResponse({"success": False, "errors": form.errors})
    return JsonResponse(
        {"success": False, "message": "Неверный метод запроса"}
    )


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise ValidationError("Номер не валиден")

    return pn_normalized


class UserRegistrationView(View):
    def get(self, request):
        return redirect("app:index")

    def post(self, request):
        name = request.POST.get("FULL_NAME_CREATE")
        email = request.POST.get("EMAIL_CREATE")
        password = request.POST.get("PASSWORD_CREATE")
        try:
            user = get_user_model().objects.create_user(
                email=email, username=email, password=password
            )
            Client.objects.create(full_name=name, user=user)
        except IntegrityError:
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "Пользователь с таким email уже зарегистрирован",
                }
            )
        login(request, user)

        return JsonResponse({"success": True})


class UserLoginView(View):
    def get(self, request):
        return redirect("app:index")

    def post(self, request):
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
        else:
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "Неверно указаны email или пароль",
                }
            )

        return JsonResponse({"success": True})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("app:index")


class UserProfileView(View):
    def get(self, request):
        user = request.user
        orders = Order.objects.filter(client__user=user).select_related(
            "box", "box__storage", "box__storage__address"
        )
        curr_orders = []
        closed_orders = []

        for order in orders:
            if order.status == 3:
                closed_orders.append(order)
            else:
                days_to_expire = (
                    (order.expiration - date.today()).total_seconds()
                ) / 86400
                days_to_add_expire = order.expiration + timedelta(days=182)
                curr_orders.append(
                    {
                        "order": order,
                        "days_to_expire": days_to_expire,
                        "days_to_add_expire": days_to_add_expire,
                    }
                )

        context = {
            "current_orders": curr_orders,
            "closed_orders": closed_orders,
        }

        return render(request, "profile.html", context)

    def post(self, request):
        if request.POST.get("extend_rent_time"):
            order_id = int(request.POST.get("order_id"))
            new_rent_end_date = datetime.strptime(
                request.POST.get("new_rent_end_date"), "%Y-%m-%d"
            ).date()
            Order.objects.filter(pk=order_id).update(
                expiration=new_rent_end_date
            )

            return JsonResponse({"success": True})

        if request.POST.get("open_box"):
            order_id = int(request.POST.get("order_id"))
            order = Order.objects.get(pk=order_id)

            img_url = request.build_absolute_uri("/media/qr.png")
            subject = f"QR-код для открытия бокса {order.box.number}"
            html_message = f"""<p>Здравствуйте, {order.client.full_name}<br>
Ваш QR-код для открытия бокса {order.box.number} по адресу {order.box.storage.address}.<br>
Аренда завершена.</p>
<p>Ждем вас снова!</p>
<img src='{img_url}'>"""
            send_mail(
                subject,
                "",
                settings.EMAIL_HOST_USER,
                [order.client.user.email],
                html_message=html_message,
            )

            order.status=3
            order.save()
            order.box.is_occupied=False
            order.box.save()

            return JsonResponse({"success": True})

        email = request.POST.get("EMAIL_EDIT")
        phone = request.POST.get("PHONE_EDIT")
        password = request.POST.get("PASSWORD_EDIT")
        user = request.user
        client = request.user.client

        try:
            phone_number = normalise_phone_number(phone)
        except (ValidationError, NumberParseException):
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "Введен неверный телефонный номер",
                }
            )

        if user.email != email:
            user.email = email
            user.username = email
            user.save()

        if not user.check_password(password):
            user.set_password(password)
            user.save()

        if client.phone_number != phone_number:
            client.phone_number = phone
            client.save()

        return JsonResponse({"success": True})
