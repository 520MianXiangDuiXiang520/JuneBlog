import datetime
import sys
import time
from arrange import Arrange
from generate_report import GetReport
from utils.email_utils import EmailUtil
from utils.deamon import Daemon
import Setting


class SendRegularly(Daemon):
    def _run(self):
        while True:
            if datetime.datetime.now().strftime("%H") == Setting.START_TIME:
                try:
                    data = Arrange().arrange()
                    if len(data) > 0:
                        report = GetReport.get_report(data)
                        subject = f'{(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}' \
                                  f'站点访问情况汇总'
                        EmailUtil.send(report, subject)
                except Exception as e:
                    print(e)
                    print("="*20)
                    print()
            time.sleep(60 * 60)


if __name__ == "__main__":
    daemon = SendRegularly('/tmp/process.pid', stdout=Setting.LOG_FILE_PATH )
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print('unknown command')
            sys.exit(2)
        sys.exit(0)
    else:
        print('usage: %s start|stop|restart' % sys.argv[0])
        sys.exit(2)
