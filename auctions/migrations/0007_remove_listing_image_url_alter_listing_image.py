# Generated by Django 4.2.3 on 2023-08-05 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
