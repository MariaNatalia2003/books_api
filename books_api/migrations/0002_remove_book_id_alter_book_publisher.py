# Generated by Django 5.2.4 on 2025-07-10 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='id',
        ),
        migrations.AlterField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, default='', max_length=50, primary_key=True, serialize=False),
        ),
    ]
