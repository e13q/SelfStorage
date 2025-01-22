from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import CustomUser, Client, FAQ, Address, Warehouse, Box, Order
from datetime import date


class Command(BaseCommand):
    help = "Заполнить базу данных тестовыми данными"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            with open("./static/img/image11.png", "rb") as f:
                warehouse_1 = Warehouse.objects.create(
                    address=Address.objects.create(
                        city='Москва',
                        street_address='ул. Рокотова, д. 15'
                    ),
                    advantage='Рядом с метро',
                    temperature=17,
                    ceiling=3.5,
                    image=File(f)
                )
            with open("./static/img/image2.png", "rb") as f:
                warehouse_2 = Warehouse.objects.create(
                    address=Address.objects.create(
                        city='Одинцово',
                        street_address='ул. Северная, д. 36'
                    ),
                    advantage='Парковка',
                    temperature=18,
                    ceiling=3.5,
                    image=File(f)
                )
            with open("./static/img/image15.png", "rb") as f:
                warehouse_3 = Warehouse.objects.create(
                    address=Address.objects.create(
                        city='Пушкино',
                        street_address='ул. Строителей, д. 5'
                    ),
                    advantage='Высокие потолки',
                    temperature=20,
                    ceiling=5.5,
                    image=File(f)
                )
            with open("./static/img/image151.png", "rb") as f:
                warehouse_4 = Warehouse.objects.create(
                    address=Address.objects.create(
                        city='Люберцы',
                        street_address='ул. Советская, д. 88'
                    ),
                    advantage='Осталось мало боксов',
                    temperature=18,
                    ceiling=3.5,
                    image=File(f)
                )
            with open("./static/img/image16.png", "rb") as f:
                warehouse_5 = Warehouse.objects.create(
                    address=Address.objects.create(
                        city='Домодедово',
                        street_address='ул. Орджоникидзе, д. 29'
                    ),
                    advantage='Большие боксы',
                    temperature=21,
                    ceiling=4.5,
                    image=File(f)
                )

            user1 = CustomUser.objects.create_user(
                email="user1@example.com", password="password123", username="user1"
            )
            user2 = CustomUser.objects.create_user(
                email="user2@example.com", password="password123", username="user2"
            )

            client1 = Client.objects.create(
                full_name="Иван Иванов",
                user=user1,
                phone_number="+79161112233"
            )
            client2 = Client.objects.create(
                full_name="Петр Петров",
                user=user2,
                phone_number="+79162223344"
            )

            FAQ.objects.create(question="Как арендовать склад?", answer="Обратитесь к нам по телефону.")
            FAQ.objects.create(question="Какие условия аренды?", answer="Смотрите наш договор.")


            box_1 = Box.objects.create(
                number="№1389-11",
                storage=warehouse_1,
                floor=1,
                length=2,
                width=1,
                height=2.5,
                price=2264.00,
                is_occupied=False
            )
            box_2 = Box.objects.create(
                number="№2389-13",
                storage=warehouse_1,
                floor=2,
                length=2,
                width=2,
                height=2.5,
                price=2561.00,
                is_occupied=False
            )
            box_3 = Box.objects.create(
                number="№1234-56",
                storage=warehouse_2,
                floor=1,
                length=2,
                width=4,
                height=2.5,
                price=1234.00,
                is_occupied=False
            )
            box_4 = Box.objects.create(
                number="№2345-67",
                storage=warehouse_2,
                floor=2,
                length=5,
                width=2,
                height=2,
                price=2345.00,
                is_occupied=False
            )
            box_5 = Box.objects.create(
                number="№3456-78",
                storage=warehouse_3,
                floor=2,
                length=4,
                width=4,
                height=2,
                price=3456.00,
                is_occupied=False
            )
            box_6 = Box.objects.create(
                number="№4567-89",
                storage=warehouse_3,
                floor=2,
                length=5,
                width=2,
                height=2,
                price=4567.00,
                is_occupied=False
            )
            box_7 = Box.objects.create(
                number="№5678-90",
                storage=warehouse_4,
                floor=2,
                length=5,
                width=2,
                height=2,
                price=5678.00,
                is_occupied=False
            )
            box_8 = Box.objects.create(
                number="№6789-10",
                storage=warehouse_4,
                floor=2,
                length=5,
                width=3,
                height=3,
                price=6789.00,
                is_occupied=False
            )
            box_9 = Box.objects.create(
                number="№7890-11",
                storage=warehouse_5,
                floor=3,
                length=5,
                width=2,
                height=1,
                price=7890.00,
                is_occupied=False
            )
            box_10 = Box.objects.create(
                number="№8901-23",
                storage=warehouse_5,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=False
            )
            box_11 = Box.objects.create(
                number="№7891-14",
                storage=warehouse_5,
                floor=3,
                length=5,
                width=2,
                height=1,
                price=7890.00,
                is_occupied=True
            )
            box_12 = Box.objects.create(
                number="№8901-41",
                storage=warehouse_3,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=True
            )
            box_13 = Box.objects.create(
                number="№8123",
                storage=warehouse_3,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=True
            )
            box_14 = Box.objects.create(
                number="№81125",
                storage=warehouse_4,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=True
            )
            box_15 = Box.objects.create(
                number="№124",
                storage=warehouse_2,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=True
            )
            box_16 = Box.objects.create(
                number="№4121-4412",
                storage=warehouse_4,
                floor=3,
                length=5,
                width=4,
                height=1,
                price=8901.00,
                is_occupied=True
            )

            Order.objects.create(
                status=2,
                date=date(2024, 6, 1),
                box=box_11,
                client=client2,
                address="Нейтральные воды",
                expiration=date(2025, 5, 24)
            )
            Order.objects.create(
                status=2,
                date=date(2024, 6, 1),
                box=box_12,
                client=client2,
                address="В тридевятом царстве",
                expiration=date(2025, 5, 24)
            )
            Order.objects.create(
                status=2,
                date=date(2024, 6, 1),
                box=box_13,
                client=client2,
                address="В Ялте",
                expiration=date(2025, 5, 24)
            )
            Order.objects.create(
                status=1,
                date=date(2024, 6, 1),
                box=box_14,
                client=client1,
                address="На Луне",
                expiration=date(2025, 1, 21)
            )
            Order.objects.create(
                status=1,
                date=date(2025, 1, 1),
                box=box_15,
                client=client1,
                address="Улица Пушкина, дом Пушкина, город Пушкина",
                expiration=date(2025, 1, 1)
            )
            Order.objects.create(
                status=1,
                date=date(2024, 6, 1),
                box=box_16,
                client=client1,
                address="Где-то далеко на проспекте Ленина",
                expiration=date(2025, 1, 12)
            )
            self.stdout.write(
                self.style.SUCCESS("Тестовые данные успешно загружены в бд")
            )
