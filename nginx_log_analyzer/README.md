# README

这是一个通过分析 Nginx 日志统计每天站点访问情况的脚本，统计结果会以邮件的方式通知你

## 怎么用？

1. 保证 python 版本在 3.7 以上
2. 下载依赖： `pip install requirements.txt`
3. 配置 Setting.py
4. 执行 `python3 run.py start` 启动脚本
   * 停止脚本： `python3 run.py stop`
   * 重启脚本： `python3 run.py restart`
   * 感谢 https://blog.csdn.net/chenbogger/article/details/99312582

## 怎么工作的？

* `readLog.py`负责读取 Log 文件
* `analyzer.py` 负责解析 log 文件中的每一行日志, Nginx自定义access日志格式可以修改 `SimpleAnalyzer`类或自定义一个类,继承`Analyzer`, 并实现它的 `analysis_strategy`, 并将每一行解析出的结果保存在`self.data`中，这是一个`dict`, `self.data`的 key 应该是 `self.all_fields`中的元素。如果使用自定义的派生类，需要修改 `Setting.FILE_NAME` 和 `Setting.CLASS_NAME`
* `arrange.py` 负责整理 `analyzer.py` 解析出的数据
* `generate_report.py` 负责将 `arrange.py` 整理出的结果格式化为字符串，作为邮件正文。

## Redis？

对每个客户端IP，我查询了它的归属地，并将查询结果保存到了 Redis 中，如果不需要，可以设置 `Setting.IP_ADDR_CACHE = False` 或 通过修改 `Analyzer`的派生类取消。