# Generated by Django 4.1.4 on 2023-01-23 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('post_board', '0003_reply_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
