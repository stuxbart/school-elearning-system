# Generated by Django 3.1.7 on 2021-03-15 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gradebook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentsubjectrecordbook',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]