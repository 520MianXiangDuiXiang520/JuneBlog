from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Article, Tags


class ArticleSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()
    detail = serializers.HyperlinkedIdentityField(view_name='detail', source='id', lookup_url_kwarg="detail")

    def get_create_time(self, row):
        return row.create_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'abstract', 'tags', 'detail']
        depth = 1


class ArticleDetailSerializer(serializers.ModelSerializer):
    create_time = serializers.SerializerMethodField()

    def get_create_time(self, row):
        return row.create_time.strftime("%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Article
        fields = ['id', 'title', 'create_time', 'tags', 'article']
        depth = 1


class TagsSerializer(serializers.ModelSerializer):
    num = serializers.SerializerMethodField()

    def get_num(self, row):
        return len(Article.objects.filter(tags=row))

    class Meta:
        model = Tags
        fields = ['id', 'name', 'create_time', 'num']
