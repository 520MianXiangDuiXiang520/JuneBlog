# Generated by Django 2.2.2 on 2020-02-01 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=128)),
                ('create_time', models.TimeField(auto_now_add=True)),
            ],
        ),
    ]
