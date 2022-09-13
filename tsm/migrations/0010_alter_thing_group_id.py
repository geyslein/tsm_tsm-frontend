# Generated by Django 4.0.7 on 2022-09-12 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('tsm', '0009_alter_mqttconfig_password_alter_mqttconfig_topic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thing',
            name='group_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='Project'),
        ),
    ]