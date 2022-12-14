# Generated by Django 4.1.3 on 2022-11-12 11:36

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, validators=[django.core.validators.MinLengthValidator(3)])),
                ('reps', models.PositiveIntegerField()),
                ('sets', models.PositiveIntegerField()),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('link_to_image', models.URLField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
