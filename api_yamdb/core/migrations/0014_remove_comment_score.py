# Generated by Django 3.2 on 2023-05-13 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_comment_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='score',
        ),
    ]