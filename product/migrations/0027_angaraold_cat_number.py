# Generated by Django 3.0.2 on 2020-03-25 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0026_auto_20200325_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='angaraold',
            name='cat_number',
            field=models.CharField(default=None, max_length=45),
            preserve_default=False,
        ),
    ]