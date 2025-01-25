from django import forms
from .models import Order, Client, CustomUser, Box
from phonenumber_field.formfields import PhoneNumberField
from django.db import transaction
import datetime


class OrderForm(forms.ModelForm):
    full_name = forms.CharField(
        label='',
        max_length=200,
        required=True,
        error_messages={
            'required': "Поле 'ФИО' обязательно для заполнения.",
            'invalid': "Ну и что ты тут умудрился написать?",
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'placeholder': 'ФИО'
            }
        )
    )
    email = forms.EmailField(
        label='',
        max_length=255,
        required=True,
        error_messages={
            'required': "Поле 'Email' обязательно для заполнения.",
            'invalid': "Введите корректный email-адрес.",
        },
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'placeholder': 'Электронный адрес'
            }
        )
    )
    phone_number = PhoneNumberField(
        label='',
        region="RU",
        required=True,
        error_messages={
            'invalid': "Введите правильный номер телефона в формате +7 (___) ___-__-__.",
            'required': "Поле 'Номер телефона' обязательно для заполнения.",
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'placeholder': '+7 (___) ___-__-__'
            }
        )
    )

    address = forms.CharField(
        label='',
        max_length=200,
        required=True,
        error_messages={
            'required': "Укажите откуда забирать вещи.",
        },
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'placeholder': 'Адрес откуда забираем вещи'
            }
        )
    )
    selected_box = forms.ModelChoiceField(
        label='',
        queryset=Box.objects.filter(is_occupied=False),
        required=True,
        error_messages={
            'required': "Выберите бокс для заказа",
        },
        widget=forms.Select(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'placeholder': 'Бокс'
            }
        )
    )
    order_date = forms.DateField(
        label="Начало аренды",
        required=True,
        error_messages={
            'required': "Укажите, когда начинается аренда",
        },
        widget=forms.DateInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'type': 'date',
                'placeholder': datetime.date.today().strftime('%Y-%m-%d')  # Текущая дата в формате YYYY-MM-DD
            }
        )
    )
    expiration = forms.DateField(
        label="Дата окончания аренды",
        required=True,
        error_messages={
            'required': "Укажите, когда заканчивается аренда",
        },
        widget=forms.DateInput(
            attrs={
                'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
                'type': 'date',
                'placeholder': datetime.date.today().strftime('%Y-%m-%d')  # Текущая дата в формате YYYY-MM-DD
            }
        )
    )

    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'address', 'selected_box', 'order_date', 'expiration']

    def clean(self):
        cleaned_data = super().clean()
        order_date = cleaned_data.get("order_date")
        expiration = cleaned_data.get("expiration")

        now_minus_day = datetime.datetime.now() - datetime.timedelta(days=1)
        now_minus_day = now_minus_day.date()

        if order_date and order_date < now_minus_day:
            self.add_error("order_date", "Дата начала аренды должна быть актуальной.")

        if expiration and expiration < now_minus_day:
            self.add_error("expiration", "Дата окончания аренды должна быть актуальной.")

        if order_date and expiration and expiration < order_date:
            self.add_error("expiration", "Дата окончания аренды не может быть раньше даты начала аренды.")

        return cleaned_data


    def save(self):
        with transaction.atomic():
            full_name = self.cleaned_data['full_name']
            email = self.cleaned_data['email']
            phone_number = self.cleaned_data['phone_number']
            address = self.cleaned_data['address']
            selected_box = self.cleaned_data['selected_box']
            order_date = self.cleaned_data['order_date']
            expiration = self.cleaned_data['expiration']

            user, _ = CustomUser.objects.get_or_create(email=email)
            client, _ = Client.objects.get_or_create(
                user=user,
                defaults={
                    "full_name": full_name,
                    "phone_number": phone_number
                }
            )
            order, _ = Order.objects.get_or_create(
                client=client,
                box=selected_box,
                date=order_date,
                address=address,
                expiration=expiration
            )
            selected_box.is_occupied = True
            selected_box.save()
            return order
