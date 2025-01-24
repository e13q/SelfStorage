import phonenumbers as ph
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Min, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.db.utils import IntegrityError
from .models import Box, Warehouse


def index(request):
    return render(request, 'index.html')


def boxes(request):

    warehouses = Warehouse.objects.annotate(
        total_boxes=Count('box'),
        free_boxes=Count('box', filter=Q(box__is_occupied=False)),
        min_price_box=Min('box__price')
    )

    context = {
        'warehouses': warehouses,
    }
    return render(request, 'boxes.html', context)


def rent(request):
    return render(request, 'my-rent.html')


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
        email = request.POST.get("EMAIL_CREATE")
        password = request.POST.get("PASSWORD_CREATE")

        User = get_user_model()
        try:
            user = User.objects.create(
                email=email, username=email, password=password
            )
            user.save()
        except IntegrityError:
            return JsonResponse({"success": False, "error_message": "Пользователь с таким email уже зарегистрирован"})
        login(request, user)

        return JsonResponse({"success": True})


class UserLoginView(View):
    def get(self, request):
        return redirect("app:index")

    def post(self, request):
        email = request.POST.get("EMAIL")
        password = request.POST.get("PASSWORD")

        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error_message": "Пользователь с таким email не зарегистрирован"})

        if user.password == password:
            login(request, user)
        else:
            return JsonResponse({"success": False, "error_message": "Пароль указан неверно"})

        return JsonResponse({"success": True})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("app:index")
