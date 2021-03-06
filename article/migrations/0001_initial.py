# Generated by Django 2.2.2 on 2020-01-29 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(db_column='序号', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='标签名', max_length=10, unique=True)),
                ('create_time', models.DateField(auto_now_add=True, db_column='创建时间')),
            ],
            options={
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(db_column='序号', primary_key=True, serialize=False)),
                ('title', models.CharField(db_column='标题', max_length=100)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='创建时间')),
                ('abstract', models.CharField(db_column='摘要', max_length=600)),
                ('article', models.TextField(db_column='正文')),
                ('tags', models.ManyToManyField(db_column='标签', to='article.Tags')),
            ],
            options={
                'db_table': 'article',
            },
        ),
    ]
