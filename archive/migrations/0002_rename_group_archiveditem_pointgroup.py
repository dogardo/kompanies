# Generated by Django 4.1.2 on 2024-04-19 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='archiveditem',
            old_name='group',
            new_name='pointGroup',
        ),
    ]