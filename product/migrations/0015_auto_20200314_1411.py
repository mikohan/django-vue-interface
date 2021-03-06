# Generated by Django 3.0.2 on 2020-03-14 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0014_product_one_c_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_unit', to='product.Units'),
            preserve_default=False,
        ),
    ]
