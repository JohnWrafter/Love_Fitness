# Generated by Django 4.0 on 2022-01-01 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0007_rename_plan_plans'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Plans',
            new_name='Plan',
        ),
    ]