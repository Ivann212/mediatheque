# Generated by Django 5.1.1 on 2024-10-04 18:07

import mediatheque.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mediatheque', '0011_alter_emprunt_date_retour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emprunt',
            name='date_retour',
            field=models.DateTimeField(default=mediatheque.models.date_retour_7_jours),
        ),
    ]
