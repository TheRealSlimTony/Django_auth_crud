# Generated by Django 3.2.18 on 2023-04-04 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointing_poker', '0003_auto_20230403_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='voted',
            field=models.BooleanField(default=False),
        ),
    ]
