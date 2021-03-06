# Generated by Django 3.0.2 on 2020-03-12 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_auto_20200312_1801'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productdescription',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productvideos',
            name='product',
        ),
        migrations.AddField(
            model_name='product',
            name='attribute',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductAttribute'),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductDescription'),
        ),
        migrations.AddField(
            model_name='product',
            name='img',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductImage'),
        ),
        migrations.AddField(
            model_name='product',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.ProductVideos'),
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]
