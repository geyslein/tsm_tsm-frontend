# Generated by Django 4.0.7 on 2022-09-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsm', '0014_database_is_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawdatastorage',
            name='bucket',
            field=models.CharField(max_length=63),
        ),
    ]
