# Generated by Django 3.2.18 on 2023-04-03 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointing_poker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gamesession',
            name='description',
            field=models.CharField(default='test', max_length=200),
        ),
        migrations.AlterField(
            model_name='gamesession',
            name='name',
            field=models.CharField(default='New Game Session', max_length=200),
        ),
    ]
