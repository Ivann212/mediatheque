# Generated by Django 5.1.1 on 2024-10-04 18:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediatheque', '0010_alter_emprunt_date_retour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='date_retour',
            field=models.DateTimeField(default=datetime.datetime(2024, 10, 11, 18, 1, 58, 894375, tzinfo=datetime.timezone.utc)),
        ),
    ]
