from django.db import models

# Create your models here.


class Manager(models.Model):
    name = models.CharField(max_length=20, db_column="用户名")
    password = models.CharField(max_length=20, db_column="password")
    email = models.EmailField(max_length=50)

    class Meta:
        db_table = 'manager'


class Token(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(to=Manager, on_delete=models.CASCADE)
    token = models.CharField(max_length=128)
    create_time = models.DateTimeField(auto_now_add=True)