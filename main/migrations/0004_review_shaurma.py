# Generated by Django 5.1.3 on 2025-02-16 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_location_alter_review_options_alter_shaurma_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='shaurma',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='main.shaurma'),
        ),
    ]
