# Generated by Django 3.1.7 on 2021-09-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tblbridge',
            name='test_field',
            field=models.IntegerField(default=0),
        ),
    ]
