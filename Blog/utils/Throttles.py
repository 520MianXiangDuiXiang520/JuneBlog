from rest_framework.throttling import SimpleRateThrottle


class Throttles(SimpleRateThrottle):
    scope = 'THROTTLE'

    def get_cache_key(self, request, view):
        if not request.user:
            print("节流")
            return self.get_ident(request)
        return request.user.id
