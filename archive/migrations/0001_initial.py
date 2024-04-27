# Generated by Django 4.1.2 on 2024-04-19 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='static/images/items')),
                ('url', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=10)),
                ('txID', models.CharField(max_length=200)),
                ('pixel', models.IntegerField(default=625)),
                ('gridID', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BusinessLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='static/images/bussiness')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='tableBusiness',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('businessLine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='archive.businessline')),
            ],
        ),
        migrations.CreateModel(
            name='pointGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eight', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_eight', to='archive.archiveditem')),
                ('five', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_five', to='archive.archiveditem')),
                ('four', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_four', to='archive.archiveditem')),
                ('nine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_nine', to='archive.archiveditem')),
                ('one', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_one', to='archive.archiveditem')),
                ('seven', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_seven', to='archive.archiveditem')),
                ('six', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_six', to='archive.archiveditem')),
                ('table_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blocks', to='archive.tablebusiness')),
                ('three', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_three', to='archive.archiveditem')),
                ('two', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='group_two', to='archive.archiveditem')),
            ],
        ),
        migrations.AddField(
            model_name='archiveditem',
            name='country',
            field=models.ManyToManyField(to='archive.country'),
        ),
        migrations.AddField(
            model_name='archiveditem',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group', to='archive.pointgroup'),
        ),
    ]