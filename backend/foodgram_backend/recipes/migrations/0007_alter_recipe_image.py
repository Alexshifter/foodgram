# Generated by Django 3.2.16 on 2024-07-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20240722_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default=None, null=True, upload_to='recipes/', verbose_name='Изображение к рецепту'),
        ),
    ]
