# Generated by Django 3.2.22 on 2023-12-29 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_snippet_chat_gpt_explanation'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='public_snippet',
            field=models.BooleanField(default=False),
        ),
    ]
