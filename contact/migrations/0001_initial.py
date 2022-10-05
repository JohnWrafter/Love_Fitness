# Generated by Django 4.1.1 on 2022-10-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=120)),
                ('subject', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
        ),
    ]
