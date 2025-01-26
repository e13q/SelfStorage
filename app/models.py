from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.html import format_html
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
    phone_number = PhoneNumberField(
        "Номер телефона", region="RU", blank=True
    )

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self) -> str:
        return self.full_name


class CategoryFAQ(models.Model):
    name = models.CharField("Категория", max_length=200)

    class Meta:
        verbose_name = "Категория вопросов"
        verbose_name_plural = "Категории вопросов"

    def __str__(self):
        return f"{self.name}"


class FAQ(models.Model):
    question = models.CharField("Вопрос", max_length=200)
    answer = models.TextField("Ответ")
    category = models.ForeignKey(
        CategoryFAQ,
        verbose_name="Категория",
        on_delete=models.PROTECT,
        related_name="QA"
    )

    class Meta:
        verbose_name = "Ответ на вопрос"
        verbose_name_plural = "Ответы на вопросы"

    def __str__(self):
        return f"{self.question}"


class Address(models.Model):
    street_address = models.CharField(
        max_length=255, verbose_name="Улица и номер дома"
    )
    city = models.CharField(
        max_length=100, verbose_name="Город", db_index=True
    )

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"

    def __str__(self):
        return f"{self.street_address}, {self.city}"


class Warehouse(models.Model):
    address = models.ForeignKey(
        Address, verbose_name="Адрес", on_delete=models.PROTECT
    )
    advantage = models.CharField(max_length=255, verbose_name="Преимущество")
    temperature = models.PositiveSmallIntegerField("Температура")
    ceiling = models.FloatField(
        "Предельная высота потолка, м", validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        "Баннер склада",
        upload_to="warehouse_images/",
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return f"{self.address.city}"


class WarehouseImage(models.Model):
    ordinal_number = models.PositiveIntegerField(
        verbose_name='Порядок картинки',
        default=0,
        blank=False,
        null=False,
        db_index=True
    )
    warehouse = models.ForeignKey(
        Warehouse, related_name='other_images', on_delete=models.CASCADE
    )
    image = models.ImageField(
        "Дополнительное изображение",
        upload_to="warehouse_images/",
        db_index=True,
    )

    class Meta:
        verbose_name = "Дополнительное изображение склада"
        verbose_name_plural = "Дополнительные изображения склада"
        ordering = ['ordinal_number']

    def image_preview(self):
        if self.image:
            return format_html(
                '<img src="{}" style="max-width: 255px; max-height: 200px;" />',
                self.image.url
            )
        return ''

    def __str__(self):
        return f"{self.ordinal_number} изображение для склада в {self.warehouse.address.city}"


class Box(models.Model):
    number = models.CharField("Номер", max_length=20, unique=True)
    storage = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, verbose_name="Склад"
    )
    floor = models.PositiveSmallIntegerField("Этаж")
    length = models.FloatField(
        "Длина, м",
        validators=[MinValueValidator(0)],
    )
    width = models.FloatField(
        "Ширина, м",
        validators=[MinValueValidator(0)],
    )
    height = models.FloatField(
        "Высота, м",
        validators=[MinValueValidator(0)],
    )
    price = models.DecimalField(
        "Цена аренды",
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    volume = models.FloatField("Объем", editable=False)
    is_occupied = models.BooleanField("Занят", default=False)

    @property
    def area(self):
        return self.length * self.width

    @property
    def calculated_volume(self):
        return self.length * self.width * self.height

    def save(self, *args, **kwargs):
        # Обновляем поле volume перед сохранением
        self.volume = self.calculated_volume
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def __str__(self):
        return f"{self.number} | {self.volume} м³ | {self.storage.address.city}, {self.storage.address.street_address}"


class Order(models.Model):
    STATUSES = [
        (1, "Просрочен"),
        (2, "Принят"),
        (3, "Завершен"),
    ]
    status = models.IntegerField("Статус записи", choices=STATUSES, default=2)
    date = models.DateField("Дата начала аренды")
    box = models.ForeignKey(Box, on_delete=models.PROTECT, verbose_name="Бокс")
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    address = models.TextField("Адрес", max_length=200)
    expiration = models.DateField("Дата окончания аренды")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"{self.id}"


class AdvertisingLink(models.Model):
    url = models.URLField("Ссылка")
    short_url = models.URLField("Сокращенная ссылка", blank=True)
    visits_number = models.IntegerField("Количество визитов", default=0)

    class Meta:
        verbose_name = "Рекламная ссылка"
        verbose_name_plural = "Рекламные ссылки"