import json
import uuid
from django.http import QueryDict
from django.http.response import JsonResponse
from rest_framework.views import APIView
from article.views import TagsView, ArticlesListView
from .models import Manager, Token
from Blog.utils.Tools import response_detail
from article.models import Article, Tags
from article.ArticleSerializer import ArticleDetailSerializer
from Blog.utils.Throttles import Throttles
from .Auth import AdminAuth

# Create your views here.


class TagManageView(APIView):
    throttle_classes = [Throttles]
    authentication_classes = [AdminAuth]

    @staticmethod
    def _check_tag_name(tag_name):
        assert tag_name is not None and len(tag_name) <= 10, "标签名不合法"
        try:
            Tags.objects.get(name=tag_name)
            raise AssertionError("标签已存在！")
        except Tags.DoesNotExist:
            return tag_name

    @staticmethod
    def _check_tag(tag_name):
        assert tag_name is not None, "标签名不能为空"
        try:
            return Tags.objects.get(name=tag_name)
        except Tags.DoesNotExist:
            raise AssertionError("标签不存在")

    def get(self, request, *args, **kwargs):
        return TagsView.get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        tag_name = request.POST.get('name')
        try:
            tag_name = self._check_tag_name(tag_name)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        Tags(name=tag_name).save()
        return self.get(request, args, kwargs)

    def delete(self, request, *args, **kwargs):
        tag_name = QueryDict(request.body).dict().get("tag_name")
        try:
            tag = self._check_tag(tag_name)
            tag.delete()
            return self.get(request, args, kwargs)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))


class LoginView(APIView):
    throttle_classes = [Throttles]

    def post(self, request, *args, **kwargs):
        """
        管理员登录
        """
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = Manager.objects.get(name=username, password=password)
            token = uuid.uuid4()
            Token(token=token, user=user).save()
            return JsonResponse(response_detail(200, 'ok', {"token": token}))
        except Manager.DoesNotExist:
            return JsonResponse(response_detail(401))


class ManagerView(APIView):

    def get(self, request, *args, **kwargs):
        pass


class ArticleManage(APIView):
    authentication_classes = [AdminAuth]
    throttle_classes = [Throttles]

    @staticmethod
    def _check_title(title):
        assert title is not None, "标题不能为空"
        assert len(title) <= 100, "标题长度应控制在 1-100 字符内！"
        return title

    @staticmethod
    def _check_tags(tags):
        save_tags = []
        if not tags:
            save_tags.append(Tags.objects.get(id=4))
        else:
            try:
                tags = tags.split(",")
                assert isinstance(tags, list)
            except (json.decoder.JSONDecodeError, AssertionError):
                raise AssertionError("tags 参数错误")
            for tag in tags:
                try:
                    save_tags.append(Tags.objects.get(name=tag))
                except Tags.DoesNotExist:
                    raise AssertionError("标签不存在")
        return save_tags

    @staticmethod
    def _check_article(article):
        assert article is not None and len(article) >= 50, "正文长度至少为50字节"
        return article

    def _check_abstract(self, article: str):
        article = self._check_article(article)
        spl = article.split("<!-- more -->")
        if len(spl) < 2:
            return article[0: 100]
        return spl[0] if len(spl[0]) < 300 else spl[0][0:300]

    @staticmethod
    def _check_article_exist(article_id):
        try:
            return Article.objects.get(id=int(article_id))
        except (Article.DoesNotExist, TypeError):
            raise AssertionError("参数错误（文章不存在）")

    @staticmethod
    def get(request, *args, **kwargs):
        return ArticlesListView().get(request, args, kwargs)

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        article = request.POST.get('article')
        try:
            title = self._check_title(title)
            tags = self._check_tags(tags)
            article = self._check_article(article)
            abstract = self._check_abstract(article)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        new_article = Article(title=title, article=article, abstract=abstract)
        new_article.save()
        for tag in tags:
            new_article.tags.add(tag)
        new_article.save()
        return JsonResponse(response_detail(
            200, 'ok', ArticleDetailSerializer(instance=new_article, many=False).data))

    def put(self, request, *args, **kwargs):
        # 获取参数
        PUT = QueryDict(request.body)
        data = PUT.dict()
        article_id = data.get("id")
        title = data.get("title")
        tags = data.get("tags")
        article = data.get("article")
        # 校验参数
        try:
            title = self._check_title(title)
            tags = self._check_tags(tags)
            abstract = self._check_abstract(article)
            article = self._check_article(article)
            article_obj = self._check_article_exist(article_id)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        # 如果数据没有改变，就不动数据库
        if article_obj.article != article:
            article_obj.article = article
        if article_obj.title != title:
            article_obj.title = title
        if article_obj.abstract != abstract:
            article_obj.abstract = abstract
        if article_obj.tags != tags:
            article_obj.tags.clear()
            for tag in tags:
                article_obj.tags.add(tag)

        article_obj.save()
        return JsonResponse(
            response_detail(200, "ok", ArticleDetailSerializer(
                instance=article_obj, many=False).data))

    def delete(self, request, *args, **kwargs):
        DELETE = QueryDict(request.body)
        data = DELETE.dict()
        article_id = data.get("id")
        try:
            article = self._check_article_exist(article_id)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        article.delete()
        return JsonResponse(response_detail(200, 'ok'))

