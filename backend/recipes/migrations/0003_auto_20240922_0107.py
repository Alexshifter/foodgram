# Generated by Django 3.2.16 on 2024-09-21 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-published'], 'verbose_name': 'рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AddField(
            model_name='recipe',
            name='published',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации'),
        ),
    ]
