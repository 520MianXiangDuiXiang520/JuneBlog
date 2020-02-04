from django.db import models

# Create your models here.


class Tags(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="序号")
    name = models.CharField(max_length=10, db_column="标签名", unique=True)
    create_time = models.DateField(auto_now_add=True, db_column="创建时间")

    class Meta:
        db_table = 'tags'


class Article(models.Model):
    id = models.BigAutoField(primary_key=True, db_column="序号")
    title = models.CharField(max_length=100, db_column="标题")
    tags = models.ManyToManyField(to=Tags, db_column="标签")
    create_time = models.DateTimeField(auto_now_add=True, db_column="创建时间")
    abstract = models.CharField(max_length=600, db_column="摘要")
    article = models.TextField(db_column="正文")

    class Meta:
        db_table = 'article'

