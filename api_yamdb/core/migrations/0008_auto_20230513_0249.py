# Generated by Django 3.2 on 2023-05-12 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20230512_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(max_length=2000, verbose_name='текст отзыва'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='описание произведения'),
        ),
    ]
