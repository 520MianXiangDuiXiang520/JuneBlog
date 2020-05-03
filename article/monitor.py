# __author: Junebao
# data:2020/3/14

from rest_framework.views import APIView
from rest_framework.throttling import BaseThrottle
from Blog.utils.RedisTool import RedisTool


class MonitorView(APIView):
    def __init__(self):
        self._redis_coon = RedisTool.redis_connection('39.96.48.152', 6379, 'redis19990805')
        super().__init__()

    def count(self, request):
        ident = BaseThrottle().get_ident(request)
        self._redis_coon

        pass

    def dispatch(self, request, *args, **kwargs):
        print(f"ip:{BaseThrottle().get_ident(request)}")
        print("重写父类dispath")
        return super().dispatch(request, args, kwargs)