# Generated by Django 2.1 on 2018-08-29 09:35

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0004_auto_20180829_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photoinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
