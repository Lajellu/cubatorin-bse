# Generated by Django 5.0.6 on 2025-07-25 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_rootcause'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rootcause',
            name='research1',
            field=models.TextField(blank=True, default='Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n'),
        ),
        migrations.AlterField(
            model_name='rootcause',
            name='research2',
            field=models.TextField(blank=True, default='Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n'),
        ),
        migrations.AlterField(
            model_name='rootcause',
            name='research3',
            field=models.TextField(blank=True, default='Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n'),
        ),
        migrations.AlterField(
            model_name='rootcause',
            name='research4',
            field=models.TextField(blank=True, default='Why are labs necessary? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\nWhy...? Because...\n'),
        ),
    ]
