from django.http import JsonResponse
from rest_framework.pagination import CursorPagination, PageNumberPagination, LimitOffsetPagination
from rest_framework.settings import api_settings

from Blog.utils.Tools import response_detail


class MyCursorPagination(CursorPagination):
    """
    只能看这一页和上一页,用于加载文章评论
    """
    cursor_query_param = 'cursor'
    ordering = 'id'
    page_size = 5
    page_size_query_param = "size"
    max_page_size = 10

    def get_paginated_response(self, data):
        return JsonResponse(
            response_detail(200, "ok", {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }))


class MyPageNumberPagination(PageNumberPagination):
    page_size = api_settings.PAGE_SIZE
    page_query_param = 'page'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = ('last',)

    def get_paginated_response(self, data):
        return JsonResponse(
            response_detail(200, "ok", {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }))


class MyPageNumberPagination2(PageNumberPagination):
    page_size = 4
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return JsonResponse(
            response_detail(200, "ok", {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }))


class MyLimitOffsetPagination(LimitOffsetPagination):
    """
    从第几个看后面的
    """
    default_limit = api_settings.PAGE_SIZE
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = None

    def get_paginated_response(self, data):
        return JsonResponse(
            response_detail(200, "ok", {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'results': data
            }))

