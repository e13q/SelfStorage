import random
from django.core.files import File
from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import CustomUser, Client, FAQ, Address, Warehouse, Box, Order, WarehouseImage, CategoryFAQ
from datetime import date, timedelta
from django.utils.crypto import get_random_string
from django.utils.timezone import now


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
            with open("./static/img/image11.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=1,
                    warehouse=warehouse_1,
                    image=File(f)
                )
            with open("./static/img/image__11.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=2,
                    warehouse=warehouse_1,
                    image=File(f)
                )
            with open("./static/img/image9.png", "rb") as f:
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
            with open("./static/img/image9.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=1,
                    warehouse=warehouse_2,
                    image=File(f)
                )
            with open("./static/img/image__9.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=2,
                    warehouse=warehouse_2,
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
            with open("./static/img/image15.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=1,
                    warehouse=warehouse_3,
                    image=File(f)
                )
            with open("./static/img/image__15.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=2,
                    warehouse=warehouse_3,
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
            with open("./static/img/image151.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=1,
                    warehouse=warehouse_4,
                    image=File(f)
                )
            with open("./static/img/image__151.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=2,
                    warehouse=warehouse_4,
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
            with open("./static/img/image16.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=1,
                    warehouse=warehouse_5,
                    image=File(f)
                )
            with open("./static/img/image__16.png", "rb") as f:
                WarehouseImage.objects.create(
                    ordinal_number=2,
                    warehouse=warehouse_5,
                    image=File(f)
                )

            user1 = CustomUser.objects.create_user(
                email="user1@example.com", password="password123", username="user1"
            )
            user2 = CustomUser.objects.create_user(
                email="user2@example.com", password="password123", username="user2"
            )
            user3 = CustomUser.objects.create_user(
                email="user3@example.com", password="password123", username="VALERA"
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
            client3 = Client.objects.create(
                full_name="Валерий",
                user=user3,
                phone_number="+79162223324"
            )
            cat1 = CategoryFAQ.objects.create(
                name='О складах и боксах'
            )
            cat2 = CategoryFAQ.objects.create(
                name='Доступ к складам и боксам'
            )
            cat3 = CategoryFAQ.objects.create(
                name='Договор аренды и оплата'
            )
            FAQ.objects.create(question="Как устроены склады индивидуального хранения SelfStorage?", answer="Каждый склад сети SelfStorage – это отапливаемое и сухое помещение, оборудованное боксами различных размеров, которые вы можете арендовать для хранения вещей на любой срок от 1 месяца.", category=cat1)
            FAQ.objects.create(question="Какие условия хранения поддерживаются в складах SelfStorage?", answer="Во всех филиалах Кладовкин регулярно проводится уборка помещений, а также поддерживается постоянная температура и уровень влажности.", category=cat1)
            FAQ.objects.create(question="Какие меры безопасности соблюдаются в складах SelfStorage?", answer="Все складские помещения оборудованы электронной системой доступа по пин-коду, поэтому попасть на склад могут только арендаторы и доверенные лица. Более того, все склады находятся под видеонаблюдением, а служба круглосуточной заботы о клиентах Кладовкин осуществляет мониторинг и реагирование на нестандартные ситуации.", category=cat1)
            FAQ.objects.create(question="Чем, помимо местоположения, отличаются склады сети SelfStorage между собой?", answer="Наши склады бывают двух типов: автоматизированные и с администратором. Более того, каждый склад обладает некоторыми особенностями. Так, например, в некоторых складах есть возможность подъехать к боксу прямо на машине, в других прилегающая к складу территория обустроена под парковку. Чтобы найти подходящий под свои потребности склад, переходите на страницу Боксы и цены с возможностью настроить фильтрацию по ключевым характеристикам.", category=cat1)
            FAQ.objects.create(question="Боксы каких размеров можно арендовать в SelfStorage?", answer="Мы предлагаем широкий выбор боксов разных размеров площадью от 1 до 50 м2. Выбирая бокс, обратите внимание на высоту потолков, параметры бокса и дверного проёма, а чтобы точно не ошибиться с выбором, ознакомьтесь с нашими материалами на странице Как выбрать бокс или получите консультацию специалиста.", category=cat1)
            FAQ.objects.create(question="Что нельзя хранить в боксах SelfStorage?", answer="Мы не принимаем на хранение следующие позиции: токсичные и радиоактивные вещества; материалы, источающие дым и запах; легковоспламеняющиеся материалы и жидкости; запрещенные к обороту в РФ предметы; оружие и взрывоопасные вещества; деньги и ценные бумаги; продукты питания; растения и животные; лекарственные препараты в любой форме. Будьте внимательны: оформляя договор аренды, вы соглашаетесь с этими условиями и берёте на себя полную ответственность за содержимое бокса.", category=cat1)
            FAQ.objects.create(question="Что такое антресольный бокс?", answer="Боксы антресольного типа представляют собой ячейки, расположенные выше уровня пола, как правило, на высоте около 2 метров. Доступ к таким боксам осуществляется с помощью передвижных лестниц-платформ, которые доступны всем арендаторам.", category=cat1)
            FAQ.objects.create(question="Как перевезти, погрузить и разгрузить вещи?", answer="Вы можете перевезти вещи самостоятельно или воспользоваться услугами доставки: SelfStorage: Закажите услугу перевозки вещей под ключ, а мы бережно упакуем, погрузим и перевезем ваши вещи на склад. Яндекс Go: Закажите грузовое такси, чтобы перевезти вещи в самые сжатые сроки. Яндекс.Драйв: Воспользуйтесь услугами грузового каршеринга, чтобы перевезти вещи самостоятельно.", category=cat1)
            FAQ.objects.create(question="Как осуществляется доступ к боксу?", answer="Бокс – это ваш личный мини-склад, расположенный в складском комплексе SelfStorage. В полностью автоматизированных складах боксы оборудованы электронной системой доступа по пин-коду, который вы получите по СМС сразу после заключения договора аренды. Пин-код нужно будет ввести в специальный терминал на территории складского комплекса, после чего доступ к вашему личному мини-складу будет открыт. В складах с администратором боксы закрываются на навесной замок, ключ от которого находиться только у арендатора. Вы можете использовать свой замок или приобрести новый прямо на складе, наши менеджеры помогут вам с выбором.", category=cat2)
            FAQ.objects.create(question="Как осуществляется доступ к складскому комплексу?", answer="Все наши складские комплексы оборудованы электронной системой доступа. Оформив договор аренды онлайн, вы получите СМС на свой телефон с персональным кодом доступа к складу. Полученный пин-код нужно будет ввести в специальное поле в мобильном приложении или в терминал, расположенный рядом с входной дверью в комплекс, после чего доступ будет открыт. Код доступа вы всегда сможете найти в своём личном кабинете на сайте или в мобильном приложении.", category=cat2)
            FAQ.objects.create(question="В какое время можно попасть на склад и воспользоваться арендованным боксом?", answer="Мы стремимся сделать процесс использования боксов максимально комфортным, поэтому все филиалы Кладовкин, кроме склада Румянцево, работают круглосуточно и без выходных. Пользуйтесь боксом в любое время как своей личной кладовкой, привозите и забирайте вещи тогда, когда вам удобно.", category=cat2)
            FAQ.objects.create(question="Что произойдет, если я забуду свой пин-код?", answer="Вы всегда можете найти код доступа в своем личном кабинете сайте или в мобильном приложении. Если вы утратите доступ к своему личному кабинету, мы поможем вам восстановить аккаунт и обновим пин-код в целях безопасности. Для этого вам, арендатору, необходимо приехать в офис Кладовкин и предъявить ваше удостоверение личности с фотографией.", category=cat2)
            FAQ.objects.create(question="Могу ли я посмотреть бокс перед заключением договора аренды?", answer="Вы можете приехать и посмотреть лично, как всё устроено на складах Кладовкин и в каждом конкретном боксе. Для этого вам нужно оформить гостевой визит, заполнив форму на странице интересующего вас бокса. После заполнения контактных данных вам на телефон придет СМС с одноразовым кодом доступа в складской комплекс, которым вы сможете воспользоваться в течение 7 дней после получения.", category=cat2)
            FAQ.objects.create(question="Могу ли я разрешить другим лицам доступ к моему боксу?", answer="В Кладовкин вы можете пользоваться боксом вместе с другими людьми: членами семьи, коллегами или друзьями. Для этого вам нужно поделиться ключом от своего навесного замка или пин-кодом от электромеханического. Не забудьте сообщить код доступа к складскому помещению.", category=cat2)
            FAQ.objects.create(question="Могу ли я поменять пин-код от своего бокса?", answer="Конечно! Поменять пин-код от своего бокса вы можете по телефону службы круглосуточной заботы о клиентах Кладовкин или в нашем офисе.", category=cat2)
            FAQ.objects.create(question="Как арендовать помещение для хранения в SelfStorage?", answer="Чтобы арендовать бокс, вам нужно зарегистрироваться в личном кабинете, выбрать подходящий тариф и оплатить услуги. Всё это вы можете сделать онлайн, по телефону службы круглосуточной заботы о клиентах Кладовкин или в нашем офисе. Чтобы узнать подробнее о процедуре аренды бокса, переходите на страницу Как выбрать бокс или получите консультацию специалиста.", category=cat3)
            FAQ.objects.create(question="Какой минимальный и максимальный срок аренды бокса?", answer="Вы можете арендовать бокс на любой срок от 1 месяца. Договор аренды заключается на срок до 11 месяцев с последующим автоматическим продлением до того момента, пока вы не захотите его расторгнуть.", category=cat3)
            FAQ.objects.create(question="Нужно заключать договор аренды заранее или же можно сделать это в день привоза вещей?", answer="Заключать договор предварительно совсем не обязательно. Вы можете оформить договор онлайн в любое время суток или по приезде на склад с администратором непосредственно в день начала пользования складским помещением.", category=cat3)
            FAQ.objects.create(question="Какие документы необходимы для заключения договора аренды?", answer="Физическим лицам для заключения договора аренды понадобится только паспорт. Прикрепите фотографию или скан документа к личному кабинету, если арендуете бокс онлайн, или возьмите оригинал с собой для заключения договора в офисе. Чтобы узнать полный список документов, необходимых для заключения договора аренды юридическому лицу, получите консультацию специалиста Круглосуточной службы поддержки клиентов.", category=cat3)
            FAQ.objects.create(question="Какие способы оплаты принимает SelfStorage?", answer="Вы можете оплатить аренду бокса любым удобным способом: В личном кабинете на сайте банковской картой или через электронные кошельки; В офисе Кладовкин наличными или банковской картой; По реквизитам в отделении любого банка или онлайн. Вы можете привязать банковскую карту к своему личному кабинету и настроить ежемесячный автоматический платёж.", category=cat3)
            FAQ.objects.create(question="Нужно ли оплачивать весь срок аренды сразу?", answer="Нет, вы можете производить оплату ежемесячно, расчетным днём будет считаться дата заключения договора. Каждый месяц за 7 дней до начала нового арендного периода вам на электронную почту будет поступать счет оплаты. Вы можете производить оплату с помощью банковских карт, наличными в нашем офисе или по реквизитам в банке. Если же вы прикрепите карту к личному кабинету, оплата будет производиться автоматически в первый день нового арендного периода.", category=cat3)
            FAQ.objects.create(question="От чего зависит размер арендной ставки?", answer="Размер арендной ставки зависит от выбранного тарифного плана: чем больше предполагаемый срок аренды, тем выше скидка на стоимость бокса в месяц. В нашей компании действуют три тарифа аренды: 1 месяц, 6 месяцев и 1 год. Выбрав любой из тарифов, вы можете оплачивать аренду ежемесячно.", category=cat3)
            FAQ.objects.create(question="Как и когда можно расторгнуть договор аренды?", answer="Договор может быть расторгнут в любое время. Для этого вам нужно освободить помещение и оставить его открытым, после чего нажать кнопку Закрыть договор в личном кабинете или сообщить о расторжении договора менеджеру службы круглосуточной заботы о клиентах. Мы проверим бокс и вернем вам депозит в течение 10 рабочих дней с момента закрытия договора.", category=cat3)
            FAQ.objects.create(question="За какой срок я должен уведомить о расторжении договора?", answer="Мы просим наших клиентов сообщать нам о предполагаемой дате расторжения договора за 10 рабочих дней до момента ее наступления.", category=cat3)
            FAQ.objects.create(question="Как определяется размер обеспечительного платежа?", answer="Сумма обеспечительного платежа или, иными словами, страхового депозита составляет 50% от размера арендной ставки. Депозит оплачивается один раз при заключении договора и возвращается при его расторжении в течение 10 рабочих дней.", category=cat3)
            FAQ.objects.create(question="Срочно нужно увеличить площадь. Как быть?", answer="Если по каким-либо причинам вам нужен бокс большего или меньшего размера, на другом складе или по другой цене, вы всегда можете обратиться с вопросом в Круглосуточную службу заботы о клиентах Кладовкин. Наши специалисты помогут подобрать подходящий бокс и переоформят договор аренды.", category=cat3)

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
                length=1,
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
            today = now().date()
            for days_left in [30, 14, 7, 3]:
                Order.objects.create(
                    status=1,
                    date=today,
                    address="На Луне",
                    client=client3,
                    box=Box.objects.create(
                        number=get_random_string(6),
                        storage=warehouse_5,
                        floor=random.choice(range(1,3)),
                        length=random.choice(range(1,3)),
                        width=random.choice(range(1,3)),
                        height=random.choice(range(1,3)),
                        price=random.choice(range(1000,9000)),
                        is_occupied=True
                    ),
                    expiration=today + timedelta(days=days_left)
                )

            for overdue_days in [1, 30, 60, 90, 120, 150, 180]:
                Order.objects.create(
                    status=2,
                    date=today - timedelta(days=90),
                    address="На Земле",
                    client=client3,
                    box=Box.objects.create(
                        number=get_random_string(6),
                        storage=warehouse_5,
                        floor=random.choice(range(1,3)),
                        length=random.choice(range(1,3)),
                        width=random.choice(range(1,3)),
                        height=random.choice(range(1,3)),
                        price=random.choice(range(1000,9000)),
                        is_occupied=True
                    ),
                    expiration=today - timedelta(days=overdue_days)
                )
            self.stdout.write(
                self.style.SUCCESS("Тестовые данные успешно загружены в бд")
            )
