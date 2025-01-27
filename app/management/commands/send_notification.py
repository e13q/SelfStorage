from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from app.models import Order
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Отправляет уведомления о заказах'

    def handle(self, *args, **kwargs):
        today = now().date()
        reminder_periods = [30, 14, 7, 3]
        overdue_periods = [1, 30, 60, 90, 120, 150, 180]
        orders = Order.objects.filter(status__in=[1, 2])
        for order in orders:
            if order.status == 1 and order.expiration > today:
                for days_left in reminder_periods:
                    if order.expiration == today + timedelta(days=days_left):
                        self.send_email(
                            order.client.user.email,
                            f"Ваш заказ №{order.id} заканчивается через {days_left} дней.",
                            "SelfStorage|Напоминание о завершении аренды | {days_left} дней"
                        )
            elif order.status == 1 and order.expiration < today:
                overdue_days = (today - order.expiration).days
                order.status = 2
                order.save()
                self.send_email(
                    order.client.user.email,
                    f"Ваш заказ №{order.id} просрочен. Вещи будут храниться {180-overdue_days} дней по повышенному тарифу, после чего в случае, если вы их так и не заберете – вы их потеряете. Пожалуйста, свяжитесь с нами.",
                    "SelfStorage| Заказ просрочен"
                )
            elif order.expiration < today:
                overdue_days = (today - order.expiration).days

                # Уведомления на 30, 60, 90, 120, 150 дни
                if overdue_days in overdue_periods and overdue_days != 180:
                    self.send_email(
                        order.client.user.email,
                        f"Ваш заказ №{order.id} просрочен на {overdue_days} дней. Вещи будут храниться {180-overdue_days} дней по повышенному тарифу, после чего в случае, если вы их так и не заберете – вы их потеряете. Пожалуйста, свяжитесь с нами.",
                        f"SelfStorage| Заказ просрочен на {overdue_days} дней"
                    )

                # Последний день просрочки (180 дней)
                if overdue_days == 180:
                    order.status = 3
                    order.box.is_occupied = False
                    order.box.save()
                    order.save()
                    self.send_email(
                        order.client.user.email,
                        f"Ваш заказ №{order.id} просрочен на 180 дней. Вещи утилизированы, заказ завершен.",
                        "SelfStorage| Заказ завершен"
                    )

        self.stdout.write("Уведомления отправлены.")

    @staticmethod
    def send_email(to_email, message, subject):
        send_mail(
            subject,
            message,
            'from@example.com',
            [to_email],
            fail_silently=False,
        )
