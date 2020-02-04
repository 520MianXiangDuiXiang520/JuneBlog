from django.db import models
from article.models import Article

# Create your models here.


class Talking(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, null=True, blank=True, db_column="用户名")
    email = models.EmailField(max_length=50, db_column="email")
    talking_time = models.DateTimeField(auto_now_add=True, db_column="评论时间")
    talk = models.CharField(max_length=600, db_column="内容")
    article = models.ForeignKey(to=Article, on_delete=models.CASCADE, db_column="对应文章")
    father = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, db_column="father")

    class Meta:
        db_table = "Talking"

