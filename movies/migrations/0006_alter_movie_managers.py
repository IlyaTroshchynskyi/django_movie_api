# Generated by Django 3.2.6 on 2022-05-14 14:05

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movieimdb'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='movie',
            managers=[
                ('annotated_manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
