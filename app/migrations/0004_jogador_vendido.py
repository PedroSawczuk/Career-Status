# Generated by Django 5.0.6 on 2024-06-06 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_nacionalidadeestatistica_delete_jogadorvendido'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogador',
            name='vendido',
            field=models.BooleanField(default=False),
        ),
    ]
