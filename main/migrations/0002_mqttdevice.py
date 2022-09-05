# Generated by Django 4.0.7 on 2022-09-05 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MqttDevice',
            fields=[
                ('type', models.CharField(choices=[('campbell_cr6', 'campbell_cr6')], default='campbell_cr6', max_length=100)),
                ('timestamp_expression', models.CharField(max_length=200)),
                ('mqtt_config', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='main.mqttconfig')),
            ],
        ),
    ]
