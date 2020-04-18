# Generated by Django 3.0.2 on 2020-04-11 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0039_auto_20200411_1936'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productattributename',
            options={'verbose_name': 'Название Атрибута', 'verbose_name_plural': 'Названия Атрибутов'},
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='attribute_value',
            field=models.CharField(max_length=45, null=True, verbose_name='Значение атрибута'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product', verbose_name='Относится к Товару'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
        migrations.AlterField(
            model_name='productdescription',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Product'),
        ),
    ]