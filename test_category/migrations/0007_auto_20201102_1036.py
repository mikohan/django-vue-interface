# Generated by Django 3.0.2 on 2020-11-02 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_category', '0006_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriesTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True)),
            ],
            options={
                'verbose_name': 'Категории2',
            },
        ),
        migrations.CreateModel(
            name='ProductTwo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('rating', models.IntegerField()),
                ('price', models.IntegerField(blank=True, null=True)),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='test_category.Brands')),
                ('categories', models.ManyToManyField(related_name='reverse_categories_two', to='test_category.CategoriesTree')),
            ],
            options={
                'verbose_name': 'Товар2',
            },
        ),
        migrations.AddField(
            model_name='categoriestree',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_reverse', to='test_category.ProductTwo'),
        ),
    ]
