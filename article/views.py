from rest_framework.views import APIView
from django.http.response import JsonResponse
from Blog.utils.Throttles import Throttles
from Blog.utils.MyPagination import MyPageNumberPagination, MyPageNumberPagination2
from .models import Article, Tags
from .ArticleSerializer import ArticleSerializer, ArticleDetailSerializer, TagsSerializer
from Blog.utils.Tools import response_detail

# Create your views here.


class TagsView(APIView):
    throttle_classes = [Throttles]

    def get(self, request, *args, **kwargs):
        tags = Tags.objects.all()
        tags_serializer = TagsSerializer(instance=tags, many=True)
        return JsonResponse(response_detail(200, 'ok', tags_serializer.data))


class ArticlesListView(APIView):
    throttle_classes = [Throttles]

    def get(self, request, *args, **kwargs):
        try:
            get_tag = int(request.GET.get("tag"))
            tag = Tags.objects.get(id=get_tag)
        except:
            tag = None
        try:
            assert tag is not None
            articles_list = Article.objects.filter(tags=tag).order_by('-create_time')
        except:
            articles_list = Article.objects.all().order_by('-create_time')
        if request.GET.get("page") and request.GET.get("size"):
            pagination = MyPageNumberPagination()
        else:
            pagination = MyPageNumberPagination2()
        pg_articles = pagination.paginate_queryset(queryset=articles_list, request=request, view=self)
        articles_list_ser = ArticleSerializer(instance=pg_articles, context={'request': request}, many=True)
        return pagination.get_paginated_response(articles_list_ser.data)


class DetailView(APIView):
    throttle_classes = [Throttles]

    @staticmethod
    def _next_article(result, article_id):
        next_article = Article.objects.filter(id__gt=article_id).first()
        if not next_article:
            result.setdefault("next", None)
        else:
            result.setdefault("next", {
                'id': next_article.id,
                'title': next_article.title
            })
        return result

    @staticmethod
    def _previous_article(result, article_id):
        previous = Article.objects.filter(id__lt=article_id).first()
        if not previous:
            result.setdefault("previous", None)
        else:
            result.setdefault("previous", {
                    'id': previous.id,
                    'title': previous.title
                })
        return result

    def get(self, request, *args, **kwargs):
        article_id = kwargs.get("detail")
        try:
            article = Article.objects.get(id=article_id)
            ads = ArticleDetailSerializer(instance=article, many=False)
            result = dict(ads.data)
            result = self._next_article(result, article_id)
            result = self._previous_article(result, article_id)
            return JsonResponse(response_detail(200, 'ok', result), safe=False)
        except Article.DoesNotExist:
            return JsonResponse(response_detail(400, "文章不存在"), safe=False)
