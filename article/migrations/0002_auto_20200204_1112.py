# Generated by Django 2.2.2 on 2020-02-04 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(db_column='序号', db_index=True, primary_key=True, serialize=False),
        ),
    ]