import requests
import random
from utils.redis_utils import RedisUtils
import Setting


class GetAddr:
    def __init__(self):
        if Setting.IP_ADDR_CACHE:
            with RedisUtils() as cli:
                self.conn = cli

    def get_addr(self, ip: str):
        addr = 'UnKnow'
        if Setting.IP_ADDR_CACHE:
            addr = self.conn.get(f"nla:{ip}")
            if addr:
                return addr.decode('utf-8')
        url = f"http://ip-api.com/json/{ip}"
        json = requests.get(url).json()
        if json['status'] == 'success':
            addr = f"{json['countryCode']}-{json['regionName']}"
            if Setting.IP_ADDR_CACHE:
                self.conn.set(f"nla:{ip}", addr)
                self.conn.expire(f"nla:{ip}", Setting.IP_ADDR_CACHE_TTL
                                 + random.randint(0, 24 * 60 * 60))
        return addr


if __name__ == '__main__':
    print(GetAddr().get_addr("42.93.195.216"))
