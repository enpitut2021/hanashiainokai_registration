# Generated by Django 3.2.5 on 2022-01-07 07:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_participants_schedule_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='participants',
            field=models.CharField(default='', max_length=37, validators=[django.core.validators.RegexValidator(message='name#0000の形式で入力してください', regex='^.{3,32}#[0-9]{4}$')], verbose_name='Discordユーザ名'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='creator',
            field=models.CharField(default='', max_length=37, validators=[django.core.validators.RegexValidator(message='name#0000の形式で入力してください', regex='^.{3,32}#[0-9]{4}$')], verbose_name='Discordユーザ名'),
        ),
    ]
