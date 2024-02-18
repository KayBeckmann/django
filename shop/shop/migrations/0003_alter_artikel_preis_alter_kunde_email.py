# Generated by Django 4.2.9 on 2024-02-18 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_artikel_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artikel',
            name='preis',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='kunde',
            name='email',
            field=models.EmailField(max_length=128, null=True),
        ),
    ]
