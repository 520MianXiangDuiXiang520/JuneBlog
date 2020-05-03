# __author: Junebao
# data:2020/3/14

import redis


class RedisTool:
    @staticmethod
    def redis_connection(address: str, port: int, password: str):
        """
        用来连接Redis
        Args:
            address: Redis 服务端IP地址
            port: [int] Redis 服务端口
            password: Redis client 登录凭证
        Return:
            type[Redis]: 返回一个redis对象
        """
        return redis.StrictRedis(address, port, password=password)