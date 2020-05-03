# 用来整理 analyzer.py 中得到的日志中的数据，并保存到 Redis 中
from utils.redis_utils import RedisUtils
import Setting

ONE_DAY = 24 * 60 * 60


class Arrange:
    def __init__(self):
        # with RedisUtils() as cli:
        #     self.conn = cli
        file = getattr(__import__(Setting.FILE_NAME ), Setting.CLASS_NAME)
        self.strategy = file()

    def arrange(self):
        """
        将从日志文件中读取出来的数据保存到 Redis 中
        数据存储使用 Hash, key 格式为 $remote_addr:$http_user_agent
        TTL 为 24 h
        :return:
        """
        self.strategy.analysis_strategy()
        result = {}
        for log in self.strategy.data:
            this_data = {}
            for field in self.strategy.fields:
                value = log.get(field)
                if value:
                    this_data[field] = value

            this_ip = result.get(log['remote_addr'])
            if this_ip:
                this_ua = this_ip.get(log['http_user_agent'])
                if this_ua:
                    this_ua.append(this_data)
                else:
                    this_ip[log['http_user_agent']] = [this_data]
            else:
                result[log['remote_addr']] = {
                    log['http_user_agent']: [this_data]
                }

                # key = f"{log['remote_addr']}:{log['http_user_agent']}"
                # self.conn.hset(key, field, value)
                # # 设置生存时长
                # self.conn.expire(key, ONE_DAY)
        return result


if __name__ == '__main__':
    Arrange().arrange()
