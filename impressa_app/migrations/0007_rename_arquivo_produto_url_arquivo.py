# Generated by Django 5.1.7 on 2025-06-25 18:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('impressa_app', '0006_remove_produto_url_arquivo_produto_arquivo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='arquivo',
            new_name='url_arquivo',
        ),
    ]
