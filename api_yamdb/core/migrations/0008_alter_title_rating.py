# Generated by Django 3.2 on 2023-05-12 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_title_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='rating',
            field=models.FloatField(blank=True, null=True, verbose_name='рейтинг на основе отзывов'),
        ),
    ]
