# Generated by Django 3.0.2 on 2020-02-07 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('brands', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branddictsup',
            name='brand_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='brand_supplier', to='brands.BrandsDict'),
        ),
        migrations.CreateModel(
            name='BrandsDictSup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suplier_brand_name', models.CharField(max_length=255)),
                ('brand_dict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ang_brand_name', to='brands.BrandsDict')),
            ],
        ),
    ]
