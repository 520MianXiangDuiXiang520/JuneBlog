# Generated by Django 2.2.2 on 2020-02-02 07:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talking', '0004_talking_talking_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='talking',
            name='father',
            field=models.ForeignKey(blank=True, db_column='father', null=True, on_delete=django.db.models.deletion.CASCADE, to='talking.Talking'),
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
