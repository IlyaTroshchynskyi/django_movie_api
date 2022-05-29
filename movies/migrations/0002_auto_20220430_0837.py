# Generated by Django 3.2.6 on 2022-04-30 08:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateField(default=datetime.date.today, verbose_name='Added')),
            ],
        ),
        migrations.RemoveField(
            model_name='movie',
            name='draft',
        ),
        migrations.AlterField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='movies.movie', verbose_name='фильм'),
        ),
        migrations.AlterField(
            model_name='review',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie', verbose_name='фильм'),
        ),
        migrations.AlterField(
            model_name='review',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='movies.review', verbose_name='Родитель'),
        ),
        migrations.DeleteModel(
            name='MovieShots',
        ),
        migrations.AddField(
            model_name='userwishes',
            name='movie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie'),
        ),
        migrations.AddField(
            model_name='userwishes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]