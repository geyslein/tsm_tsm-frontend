# Generated by Django 4.0.7 on 2022-09-09 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsm', '0003_rename_isactivated_thing_isactive_thing_isready_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='thing',
            old_name='isActive',
            new_name='is_active',
        ),
        migrations.RenameField(
            model_name='thing',
            old_name='isReady',
            new_name='is_ready',
        ),
    ]
