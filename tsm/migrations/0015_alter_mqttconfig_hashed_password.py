# Generated by Django 4.0.7 on 2022-09-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsm', '0014_mqttconfig_hashed_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mqttconfig',
            name='hashed_password',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]