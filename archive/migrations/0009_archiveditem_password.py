# Generated by Django 4.1.2 on 2024-04-25 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0008_tx_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='archiveditem',
            name='password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
    ]
