# Generated by Django 4.0.4 on 2022-06-01 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('token', models.CharField(max_length=255)),
                ('refresh_token', models.CharField(max_length=255)),
            ],
        ),
    ]
