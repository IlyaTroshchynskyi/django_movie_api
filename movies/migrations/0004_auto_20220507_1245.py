# Generated by Django 3.2.6 on 2022-05-07 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20220507_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='actor',
            options={'verbose_name': 'Actor', 'verbose_name_plural': 'Actors'},
        ),
        migrations.AlterModelOptions(
            name='director',
            options={'verbose_name': 'Director', 'verbose_name_plural': 'Directors'},
        ),
    ]