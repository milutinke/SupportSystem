# Generated by Django 3.1.4 on 2021-01-07 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_auto_20210108_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
