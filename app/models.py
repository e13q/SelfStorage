from django.core.validators import MinValueValidator
from django.db import models

class FAQ(models.Model):
    question = models.TextField("Вопрос", max_length=200)
    answer = models.TextField("Ответ", max_length=200)


class Storage(models.Model):
    address = models.TextField("Адрес", max_length=200)
    temperature = models.PositiveSmallIntegerField("Температура")
    ceiling = models.FloatField("Высота потолка, м",)
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
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    # client = models.ForeignKey(ClientUser)
    address = models.TextField("Адрес", max_length=200)
    expiration = models.DateField("Дата окончания аренды")
