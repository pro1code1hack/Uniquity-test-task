# Generated by Django 4.1.6 on 2023-02-09 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_explorer', '0002_csvfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csvfiles',
            name='uuid',
            field=models.UUIDField(editable=False, unique=True),
        ),
    ]