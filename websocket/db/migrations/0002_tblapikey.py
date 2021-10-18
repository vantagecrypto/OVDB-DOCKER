# Generated by Django 3.1.7 on 2021-10-18 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TBLApiKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('unique_id', models.CharField(default='', max_length=255)),
                ('api_key', models.CharField(default='', max_length=255)),
                ('permission', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'TBLAPIKEY',
                'managed': False,
            },
        ),
    ]
