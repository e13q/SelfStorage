from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    email = models.EmailField("Email", max_length=255, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Client(models.Model):
    full_name = models.CharField("ФИО", max_length=200)
    user = models.OneToOneField(CustomUser, on_delete=models.PROTECT)
    phone_number = PhoneNumberField("Номер телефона", region="RU", unique=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return self.full_name


class FAQ(models.Model):
    question = models.TextField("Вопрос", max_length=200)
    answer = models.TextField("Ответ", max_length=200)


class Storage(models.Model):
    address = models.TextField("Адрес", max_length=200)
    temperature = models.PositiveSmallIntegerField("Температура")
    ceiling = models.FloatField(
        "Высота потолка, м",
    )
    price = models.DecimalField(
        "Цена аренды",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )


class Box(models.Model):
    number = models.CharField("Номер", max_length=20)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    floor = models.PositiveSmallIntegerField("Этаж")
    length = models.DecimalField(
        "Длина, м",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
    )
    width = models.DecimalField(
        "Ширина, м",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
    )
    height = models.DecimalField(
        "Высота, м",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
    )
    price = models.DecimalField(
        "Цена аренды",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    occupied = models.BooleanField("Занят", default=False)


class Order(models.Model):
    STATUSES = [
        ("accepted", "Принят"),
        ("ended", "Завершен"),
    ]
    status = models.CharField("Статус записи", max_length=20, choices=STATUSES)
    date = models.DateField("Дата начала аренды")
    box = models.ForeignKey(Box, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    address = models.TextField("Адрес", max_length=200)
    expiration = models.DateField("Дата окончания аренды")
