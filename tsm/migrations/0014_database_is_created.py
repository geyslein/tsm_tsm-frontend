# Generated by Django 4.0.7 on 2022-09-14 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsm', '0013_database_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='is_created',
            field=models.BooleanField(default=False),
        ),
    ]