# Generated by Django 3.1.7 on 2021-09-29 15:43

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TBLUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('balance', models.FloatField(default=0)),
                ('spent', models.FloatField(default=0)),
                ('reset_link', models.CharField(default='', max_length=255)),
                ('permission', models.TextField(default='{"max_active_bridges": 1, "rate_limit_per_url": 14, "allowed_frequency": {"af1": true, "af2": true, "af3": true, "af4": true}, "allowed_file_flush": {"aff1": true, "aff2": true, "aff3": true, "aff4": true}, "available_bridges": {"ab1": true, "ab2": true, "ab3": true, "ab4": true, "ab5": true, "ab6": true, "ab7": true, "ab8": true, "ab9": true, "ab10": true}}')),
            ],
            options={
                'db_table': 'TBLUSER',
                'managed': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='TBLBridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('type', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('api_calls', models.IntegerField(default=0)),
                ('src_address', models.CharField(default='', max_length=255)),
                ('dst_address', models.CharField(default='', max_length=255)),
                ('format', models.TextField(blank=True, null=True)),
                ('frequency', models.IntegerField(default=0)),
                ('flush', models.IntegerField(default=0)),
                ('file_format', models.CharField(default='', max_length=255)),
                ('billed_calls', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_status', models.IntegerField(default=0)),
                ('monthly_usage', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'TBLBRIDGE',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TBLLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=255)),
                ('size', models.IntegerField(default=0)),
                ('date_from', models.DateTimeField(auto_now_add=True)),
                ('date_to', models.DateTimeField(auto_now_add=True)),
                ('is_full', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'TBLLOG',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TBLSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('server_setting', models.JSONField(default=dict)),
                ('max_active_bridges', models.IntegerField(default=0)),
                ('rate_limit_per_url', models.IntegerField(default=0)),
                ('allowed_frequency', models.JSONField(default=dict)),
                ('allowed_file_flush', models.JSONField(default=dict)),
                ('available_bridges', models.JSONField(default=dict)),
                ('price_setting', models.JSONField(default=dict)),
                ('smtp_setting', models.JSONField(default=dict)),
            ],
            options={
                'db_table': 'TBLSETTING',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TBLTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('mode', models.IntegerField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('balance', models.FloatField(default=0)),
                ('description', models.CharField(default='', max_length=255)),
                ('notes', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'TBLTRANSACTION',
                'managed': False,
            },
        ),
    ]
