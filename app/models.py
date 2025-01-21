from django.db import models

class FAQ(models.Model):
    question = models.TextField("Вопрос", max_length=200)
    answer = models.TextField("Ответ", max_length=200)


class Storage(models.Model):
    address = models.TextField("Адрес", max_length=200)
    temperature = models.PositiveSmallIntegerField("Температура")
    ceiling = models.FloatField("Высота потолка, м",)
    dimensions = models.CharField("Размер", max_length=20)
    price = models.DecimalField(
        "Цена аренды",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )


class Box(models.Model):
    number = models.CharField("Номер", max_length=20)
    address = models.TextField("Адрес", max_length=200)
    floor = models.PositiveSmallIntegerField("Этаж")
    volume = models.DecimalField(
        "Объем, м3",
        max_digits=4,
        decimal_places=1,
        validators=[MinValueValidator(0)],
    )
    dimensions = models.CharField("Размер", max_length=20)
    price = models.DecimalField(
        "Цена аренды",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    occupied = models.BooleanField("Занят", default=False)


class Order(models.Model):
    STATUSES = [
        ("accepted", "Принята"),
        ("ended", "Завершена"),
    ]
    status = models.CharField("Статус записи", max_length=20, choices=STATUSES)
    date = models.DateField("Дата начала аренды")
    box = models.ForeignKey(Box)
    client = models.ForeignKey(ClientUser)
    address = models.TextField("Адрес", max_length=200)
    expiration = models.DateField("Дата окончания аренды")
