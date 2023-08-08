# Generated by Django 4.2.3 on 2023-08-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_comment_time_alter_listing_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.AddField(
            model_name='category',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='category', to='auctions.listing'),
        ),
    ]