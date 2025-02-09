# Generated by Django 5.1.5 on 2025-01-27 14:47

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=255, verbose_name='Улица и номер дома')),
                ('city', models.CharField(db_index=True, max_length=100, verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
        migrations.CreateModel(
            name='AdvertisingLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Ссылка')),
                ('short_url', models.URLField(blank=True, verbose_name='Сокращенная ссылка')),
                ('visits_number', models.IntegerField(default=0, verbose_name='Количество визитов')),
            ],
            options={
                'verbose_name': 'Рекламная ссылка',
                'verbose_name_plural': 'Рекламные ссылки',
            },
        ),
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20, unique=True, verbose_name='Номер')),
                ('floor', models.PositiveSmallIntegerField(verbose_name='Этаж')),
                ('length', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Длина, м')),
                ('width', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Ширина, м')),
                ('height', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Высота, м')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена аренды')),
                ('volume', models.FloatField(editable=False, verbose_name='Объем')),
                ('is_occupied', models.BooleanField(default=False, verbose_name='Занят')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
        migrations.CreateModel(
            name='CategoryFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория вопросов',
                'verbose_name_plural': 'Категории вопросов',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region='RU', verbose_name='Номер телефона')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200, verbose_name='Вопрос')),
                ('answer', models.TextField(verbose_name='Ответ')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='QA', to='app.categoryfaq', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Ответ на вопрос',
                'verbose_name_plural': 'Ответы на вопросы',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Текущий'), (2, 'Просрочен'), (3, 'Завершен')], default=1, verbose_name='Статус записи')),
                ('date', models.DateField(verbose_name='Дата начала аренды')),
                ('address', models.TextField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('expiration', models.DateField(verbose_name='Дата окончания аренды')),
                ('box', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.box', verbose_name='Бокс')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advantage', models.CharField(max_length=255, verbose_name='Преимущество')),
                ('temperature', models.PositiveSmallIntegerField(verbose_name='Температура')),
                ('ceiling', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Предельная высота потолка, м')),
                ('image', models.ImageField(blank=True, db_index=True, upload_to='warehouse_images/', verbose_name='Баннер склада')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.address', verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.AddField(
            model_name='box',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.warehouse', verbose_name='Склад'),
        ),
        migrations.CreateModel(
            name='WarehouseImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordinal_number', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Порядок картинки')),
                ('image', models.ImageField(db_index=True, upload_to='warehouse_images/', verbose_name='Дополнительное изображение')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other_images', to='app.warehouse')),
            ],
            options={
                'verbose_name': 'Дополнительное изображение склада',
                'verbose_name_plural': 'Дополнительные изображения склада',
                'ordering': ['ordinal_number'],
            },
        ),
    ]
