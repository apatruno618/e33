# Generated by Django 3.1.1 on 2020-10-11 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20201011_1324'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='listing',
            name='photo_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]