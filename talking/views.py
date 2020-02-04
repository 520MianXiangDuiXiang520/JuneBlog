import re
from django.http import QueryDict
from rest_framework.views import APIView
from django.http.response import JsonResponse
from Blog import settings
from Blog.utils.Tools import response_detail
from Blog.utils.MyPagination import MyCursorPagination
from .models import Talking
from .talkingSerializer import TalkingSerializer
from article.models import Article
from django.core.mail import send_mail

# Create your views here.


class TalkingView(APIView):

    @staticmethod
    def _check_email(email):
        assert email is not None, "Email 为空"
        email_re = r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]" \
                   r"*[\w])?\.)+[\w](?:[\w-]*[\w])?"
        assert re.match(email_re, email) is not None, "email 格式错误"
        assert len(email) < 50, "email 长度不合法"
        return email

    @staticmethod
    def _check_username(username):
        if username:
            assert len(username) < 50, "用户名长度不合法"
        return username

    @staticmethod
    def _check_article_id(article_id):
        try:
            article_id = int(article_id)
        except (ValueError, TypeError):
            raise AssertionError("文章id不合法")
        try:
            get_article = Article.objects.get(id=article_id)
            return get_article
        except Article.DoesNotExist:
            raise AssertionError("文章不存在")

    @staticmethod
    def _check_talking(talking):
        assert talking is not None, "评论内容不能为空"
        assert len(talking) < 600, "评论内存长度应在 0 - 600 之间"
        return talking

    @staticmethod
    def _check_father_id(father_id):
        if not father_id:
            return
        try:
            return Talking.objects.get(id=int(father_id))
        except Talking.DoesNotExist:
            raise AssertionError("对应评论不存在")
        except ValueError:
            raise AssertionError("father_id格式错误")

    @staticmethod
    def _check_talking_id(talking_id):
        assert talking_id is not None, "talking_id不能为空"
        try:
            return Talking.objects.get(id=int(talking_id))
        except Talking.DoesNotExist:
            raise AssertionError("评论不存在")
        except TypeError:
            raise AssertionError("talking_id 不合法")

    @staticmethod
    def _send_email(receiver, receiver_name, talker, article, article_url, talked, detail):
        """发送邮件
        如果用户回复了某条评论，就发邮件通知原评论的作者
        Args:
            receiver: 接收者（原评论作者）的邮箱号
            receiver_name: 原作者用户名
            talker: 谁回复了原评论，username
            article: 在哪篇文章下的评论（article.id）
            article_url: 文章链接
            talked: 原评论内容
            detail: 回复内容
        Returns:
            return None
        """
        message = f'您好，{receiver_name} :\n 刚刚用户【{talker}】 ' \
                  f'回复了您在 【{article}】 下的评论（原评论：【{talked}】）\n\n' \
                  f'回复内容：【{detail}】 \n \n 快去看看把 {article_url}'
        subject = "JuneBlog博客回复"
        sender = settings.EMAIL_FROM
        assert send_mail(subject, message, sender, [receiver]) == 1, "发送失败"

    def get(self, request, *args, **kwargs):
        article_id = request.GET.get("article_id")
        try:
            article = self._check_article_id(article_id)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        talking = Talking.objects.filter(article=article)
        mcp = MyCursorPagination()
        paginate_data = mcp.paginate_queryset(queryset=talking, request=request, view=self)
        serializer_data = TalkingSerializer(instance=paginate_data, many=True)
        return mcp.get_paginated_response(serializer_data.data)

    def post(self, request, *args, **kwargs):
        """
        需要的参数：
          - email: 邮箱，必填
          - username：用户名，选填，不填默认为 email
          - article_id: 文章id， 必填
          - talking： 评论内容，必填
          - father_id: 如果是回复某人的评论的话，需要指定回复的是哪条评论
        """
        email = request.POST.get("email")
        username = request.POST.get("username")
        article_id = request.POST.get("article_id")
        talking = request.POST.get("talking")
        father_id = request.POST.get("father_id")
        try:
            email = self._check_email(email)
            username = self._check_username(username)
            article = self._check_article_id(article_id)
            talking = self._check_talking(talking)
            father = self._check_father_id(father_id)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
        if not username:
            username = email
        new_talking = Talking(email=email, username=username,
                              talk=talking, article=article, father=father)
        new_talking.save()
        if father:
            article_url = settings.ARTICLE_DETAIL_URL + str(article.id)
            try:
                self._send_email(receiver=father.email, receiver_name=father.username,
                                 talked=father.talk, talker=username, article=article.title,
                                 detail=talking, article_url=article_url)
            except AssertionError as e:
                # return JsonResponse(response_detail(400, e.args[0]))
                pass
        return JsonResponse(response_detail(200, "ok", TalkingSerializer(instance=new_talking, many=False).data))

    def delete(self, request, *args, **kwargs):
        DELETE = QueryDict(request.body).dict()
        talking_id = DELETE.get("talking_id")
        article_id = DELETE.get("article_id")
        try:
            talking = self._check_talking_id(talking_id)
            article = self._check_article_id(article_id)
            talking.delete()
            setattr(request, "GET", {"article_id": article_id})
            return self.get(request)
        except AssertionError as e:
            return JsonResponse(response_detail(400, e.args[0]))
