# Generated by Django 4.0 on 2022-01-08 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_hub', '0006_alter_fitnesshub_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='fitnesshub',
            name='name',
            field=models.CharField(max_length=254, null=True),
        ),
    ]
