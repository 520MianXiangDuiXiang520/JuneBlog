START_TIME = 23  # 脚本启动时间
LOG_FILE_PATH = "/home/junbao/nla/nginx_log_analyzer/logs/stdout.log"  # 脚本日志路径

# line 文件路径，用来记录上一次读到的行数
LINE_PATH = '/home/junbao/nla/nginx_log_analyzer/line'

# access.log 的路径
LOG_PATH = '/usr/local/nginx/logs/blogweb/access.log'
LOG_ENCODING = 'utf-8'

# Redis 相关配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'password'

# 是否开启 IP 缓存 （查询IP归属地很耗时，开启IP缓存后，
# 会使用 Redis 缓存IP归属地）
IP_ADDR_CACHE = True
IP_ADDR_CACHE_TTL = 7 * 24 * 60 * 60

# 日志分析策略
PACKAGE_NAME = 'nginx_log_analyzer'
FILE_NAME = 'analyzer'
CLASS_NAME = 'SimpleAnalyzer'

# Email 相关
FROM_EMAIL = '15364968962@163.com'    # 发件人Email
TO_EMAIL = '1771795643@qq.com'      # 收件人Email
SMTP_AUTO = 'password'    # SMTP 授权码
SMTP_SERVER = 'smtp.163.com'  # SMTP服务器
