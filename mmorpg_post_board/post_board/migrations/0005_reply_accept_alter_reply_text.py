# Generated by Django 4.1.4 on 2023-01-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_board', '0004_reply_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='reply',
            name='text',
            field=models.TextField(verbose_name='Reply'),
        ),
    ]
