# Generated by Django 4.0.7 on 2022-09-08 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0007_alter_thing_options_remove_thing_userid_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thing',
            name='project',
        ),
        migrations.AlterField(
            model_name='thing',
            name='group_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]