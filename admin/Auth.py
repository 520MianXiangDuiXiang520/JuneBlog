import datetime

import pytz
from django.http import QueryDict
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import APIException

from Blog.utils.Tools import timeout_judgment
from admin.models import Token, Manager


class AdminAuth(BaseAuthentication):
    @staticmethod
    def _delete_token(token_field):
        token_field.delete()

    def authenticate(self, request):
        if str(request.method).upper() == "GET":
            token = request.GET.get("token")
        else:
            data = QueryDict(request.body).dict()
            token = data.get("token")
        print(token)
        token_field = Token.objects.filter(token=token).first()
        if not token_field:
            raise APIException("认证失败(no token)")
        else:
            if timeout_judgment(token_field, 'create_time', '15/m'):
                self._delete_token(token_field)
                raise APIException("认证失败(token timeout)")
            user = Manager.objects.filter(id=token_field.user_id).first()
            token_field.create_time = datetime.datetime.now(tz=pytz.timezone('UTC'))
            token_field.save()
        return user, token_field
