from django.db import migrations


CATEGORY_IMAGE_FOLDERS = {
    "bodysuits": ("Product Images/Bodysuits", "bodysuit_"),
    "leggings": ("Product Images/Leggings", "leggings_"),
    "shorts_women": ("Product Images/Shorts", "shorts_"),
    "sports_bra": ("Product Images/Sports bras", "sportsbra_"),
}


def move_images_into_category_folders(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    database = schema_editor.connection.alias

    products = Product.objects.using(database).filter(
        category__name__in=CATEGORY_IMAGE_FOLDERS,
    )
    for product in products.iterator():
        folder, filename_prefix = CATEGORY_IMAGE_FOLDERS[product.category.name]
        image_name = product.image.name
        if (
            image_name
            and "/" not in image_name
            and image_name.startswith(filename_prefix)
        ):
            product.image = f"{folder}/{image_name}"
            product.save(using=database, update_fields=["image"])


def restore_flat_image_paths(apps, schema_editor):
    Product = apps.get_model("products", "Product")
    database = schema_editor.connection.alias

    products = Product.objects.using(database).filter(
        category__name__in=CATEGORY_IMAGE_FOLDERS,
    )
    for product in products.iterator():
        folder, _ = CATEGORY_IMAGE_FOLDERS[product.category.name]
        folder_prefix = f"{folder}/"
        image_name = product.image.name
        if image_name and image_name.startswith(folder_prefix):
            product.image = image_name[len(folder_prefix):]
            product.save(using=database, update_fields=["image"])
        else:
            legacy_prefix = f"{folder.removeprefix('Product Images/')}/"
            if image_name and image_name.startswith(legacy_prefix):
                product.image = image_name[len(legacy_prefix):]
                product.save(using=database, update_fields=["image"])


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_product_stock_quantity"),
    ]

    operations = [
        migrations.RunPython(
            move_images_into_category_folders,
            restore_flat_image_paths,
        ),
    ]
