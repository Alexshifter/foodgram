# Generated by Django 3.2.16 on 2024-08-31 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0020_auto_20240831_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shortlink',
            name='default_link',
        ),
        migrations.RemoveField(
            model_name='shortlink',
            name='short_code',
        ),
        migrations.AddField(
            model_name='shortlink',
            name='original_path',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='shortlink',
            name='short_code_path',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='shortlink',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='short_code_path', to='recipes.recipe'),
        ),
    ]
