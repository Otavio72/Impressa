# Generated by Django 5.1.7 on 2025-06-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('impressa_app', '0002_remove_pedido_pais'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='bairro',
            field=models.CharField(default='São Paulo', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='cidade',
            field=models.CharField(default='São Paulo', max_length=50),
            preserve_default=False,
        ),
    ]
