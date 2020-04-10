# Generated by Django 3.0.2 on 2020-04-02 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0031_auto_20200329_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plus', models.CharField(blank=True, max_length=100, null=True)),
                ('minus', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Category')),
            ],
        ),
    ]