# Generated by Django 4.0 on 2022-01-02 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0011_plan_description_plan_image_plan_image_url_plan_plan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='plans.plan'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Plans', to='plans.plan'),
        ),
    ]