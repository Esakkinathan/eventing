# Generated by Django 4.2.3 on 2023-07-10 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0003_venue_venue_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Approved'),
        ),
    ]
