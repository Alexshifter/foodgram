# Generated by Django 3.2.16 on 2024-07-22 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_newuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='avatar',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='avatars/'),
        ),
    ]
