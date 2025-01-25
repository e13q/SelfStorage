import phonenumbers as ph
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Count, Min, Q
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from .models import Box, Client, Warehouse


def index(request):
    return render(request, "index.html")


def boxes(request):
    warehouses = Warehouse.objects.annotate(
        total_boxes=Count("box"),
        free_boxes=Count("box", filter=Q(box__is_occupied=False)),
        min_price_box=Min("box__price"),
    )

    context = {
        "warehouses": warehouses,
    }
    return render(request, "boxes.html", context)


def rent(request):
    return render(request, "my-rent.html")


def normalise_phone_number(pn):
    pn_parsed = ph.parse(pn, "RU")
    if ph.is_valid_number(pn_parsed):
        pn_normalized = ph.format_number(pn_parsed, ph.PhoneNumberFormat.E164)
    else:
        raise

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
            # Client.objects.create(full_name=name, user=user)
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
        return render(request, "profile.html")

    def post(self, request):
        pass
