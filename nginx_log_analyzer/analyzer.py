# 用来分析日志文件
from error import UnrealizedException
from readLog import ReadLogFile
from utils.ua_utils import UAUtils
from get_addr_by_ip import GetAddr
import re


class Analyzer:
    def __init__(self):
        self.all_fields = (
            "bytes_sent", "body_bytes_sent", "connection",
            "connection_requests", "msec", "pipe",
            "request_length", "request_time", "status",
            "time_iso8601", "time_local", "http_referer",
            "http_user_agent", "remote_addr", "http_x_forwarded_for",
            "request", "remote_user", "request_uri"
        )
        self.fields = (
            "bytes_sent", "body_bytes_sent", "connection",
            "connection_requests", "msec", "pipe",
            "request_length", "request_time", "status",
            "time_iso8601", "time_local", "http_referer",
            "http_x_forwarded_for", "request", "remote_user",
            "request_uri"
        )
        self.logs = ReadLogFile().get_new_logs()
        self.data = []

    def analysis_strategy(self):
        """
        根据 nginx/conf/nginx.conf 中 log_format 的配置，找出每一行中
        remote_addr， time_local， status， time_local 等日志记录信息
        的值，每一行日志的分析结果作为一个字典，所有字典保存到 self.data 中
        data中的值格式应该类似：
            [
                {
                    "remote_addr": "139.118.123.34",
                     "time_local": "02/May/2020:18:32:17 +0800",
                     "status": "200"
                 },
                 # ....
            ]
        """
        # log 文件数据就是 self._logs
        raise UnrealizedException()


class SimpleAnalyzer(Analyzer):
    def __init__(self):
        super().__init__()
        self.static = ('.png', '.jpg', '.jpeg', '.gif', '.ttf', '.woff', '.js', '.css')

    def analysis_strategy(self):
        time_pat = r'\[.+\]'
        from_pat = r'FROM: [0-9.]+'
        ua_pat = r'UA: .+ 【'
        path_pat = r'【.+】'
        status_pat = r'\{[0-9]{3}\}'
        for log in self.logs:
            if len(log) <= 1:
                continue
            path_index = re.search(path_pat, log).span()
            request_uri = log[path_index[0] + 1: path_index[1] - 1]
            # 过滤掉对静态资源的访问
            if request_uri[-3:] in self.static or\
                    request_uri[-4:] in self.static or\
                    request_uri[-5:] in self.static:
                continue
            time_local_index = re.search(time_pat, log).span()
            time_local = log[time_local_index[0] + 1: time_local_index[1] - 7]
            remote_addr_index = re.search(from_pat, log).span()
            remote_addr = log[remote_addr_index[0] + 6: remote_addr_index[1]]
            ua_index = re.search(ua_pat, log).span()
            http_user_agent = log[ua_index[0] + 4: ua_index[1] - 4]

            status_index = re.search(status_pat, log).span()
            status = log[status_index[0] + 1: status_index[1] - 1]
            this_data = {
                "time_local": time_local.replace(" ", "_"),
                "remote_addr": f"{remote_addr}({GetAddr().get_addr(remote_addr)})",
                "http_user_agent": f"{UAUtils.get_os(http_user_agent)}/"
                                   f"{UAUtils.get_browser(http_user_agent)}/"
                                   f"{UAUtils.get_phone(http_user_agent)}".replace(" ", "_"),
                "request_uri": request_uri.replace(" ", "_"),
                "status": status.replace(" ", "_")
            }
            self.data.append(this_data)


if __name__ == '__main__':
    SimpleAnalyzer().analysis_strategy()
