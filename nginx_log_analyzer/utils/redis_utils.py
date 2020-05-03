import redis
import Setting


class RedisUtils:
    def __init__(self):
        self.password = Setting.REDIS_PASSWORD
        self.host = Setting.REDIS_HOST
        self.port = Setting.REDIS_PORT
        self.conn = None

    def __enter__(self):
        self.conn = redis.StrictRedis(host=self.host, port=self.port,
                                      password=self.password)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
        return False


if __name__ == '__main__':
    with RedisUtils() as cli:
        print(cli.get("nla:5.101.0.209").decode('utf-8'))
