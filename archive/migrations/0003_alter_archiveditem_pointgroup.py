# Generated by Django 4.1.2 on 2024-04-19 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0002_rename_group_archiveditem_pointgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archiveditem',
            name='pointGroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='archive.pointgroup'),
        ),
    ]
