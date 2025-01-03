# Generated by Django 5.0.6 on 2024-11-02 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20241102_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='shoe_images/')),
                ('shoe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.shoe')),
            ],
        ),
    ]
