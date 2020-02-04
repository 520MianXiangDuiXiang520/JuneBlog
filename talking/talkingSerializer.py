from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Talking


class TalkingSerializer(ModelSerializer):
    article_id = serializers.SerializerMethodField()
    time = serializers.SerializerMethodField()
    father = serializers.SerializerMethodField()

    @staticmethod
    def get_article_id(row):
        return row.article.id

    @staticmethod
    def get_time(row):
        return row.talking_time.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_father(row):
        return {
            "id": row.father.id,
            "email": row.father.email,
            "username": row.father.username
        } if row.father else None

    class Meta:
        model = Talking
        fields = ['id', 'email', 'username', 'article_id', 'talk', 'time', 'father']
        depth = 0
