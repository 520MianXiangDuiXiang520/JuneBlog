# 用来读取 Log 文件
from error import LineFileException
import Setting


class ReadLogFile:

    def _get_pre_line(self):
        try:
            with open(Setting.LINE_PATH, 'r') as fp:
                line = fp.readline()
                try:
                    self._line = int(line)
                except TypeError:
                    raise LineFileException("line 文件格式错误")
        except FileNotFoundError:
            raise FileNotFoundError("line 文件不存在")

    def _set_pre_line(self, line: int):
        try:
            with open(Setting.LINE_PATH, 'w') as fp:
                fp.write(str(line))
                self._line = line
        except FileNotFoundError:
            raise FileNotFoundError("line 文件不存在")

    def _read_logs(self):
        with open(Setting.LOG_PATH, 'r',
                  encoding=Setting.LOG_ENCODING) as fp:
            for i in range(self._line):
                fp.readline()
            return fp.readlines()

    def get_new_logs(self):
        self._get_pre_line()
        logs = self._read_logs()
        self._set_pre_line(self._line + len(logs))
        return logs

    def main(self):
        logs = self.get_new_logs()
        print(logs)


if __name__ == '__main__':
    ReadLogFile().main()
