from django.db import migrations, models
from django.db.models import F


def add_stock(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.using(schema_editor.connection.alias).update(
        stock_quantity=F("stock_quantity") + 10,
    )


def remove_stock(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    Product.objects.using(schema_editor.connection.alias).update(
        stock_quantity=F("stock_quantity") - 10,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_product_category_image_folders"),
    ]

    operations = [
        migrations.RunPython(add_stock, remove_stock),
    ]
