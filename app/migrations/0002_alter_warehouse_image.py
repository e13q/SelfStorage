# Generated by Django 5.1.5 on 2025-01-27 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='image',
            field=models.ImageField(db_index=True, upload_to='warehouse_images/', verbose_name='Баннер склада'),
        ),
    ]
