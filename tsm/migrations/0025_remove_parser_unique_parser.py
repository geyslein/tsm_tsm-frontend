# Generated by Django 4.0.8 on 2022-10-14 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tsm', '0024_alter_parser_unique_together_parser_unique_parser'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='parser',
            name='unique_parser',
        ),
    ]
