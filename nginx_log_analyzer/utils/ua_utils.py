from user_agents import parse


class UAUtils:
    @staticmethod
    def get_browser(ua: str):
        return parse(ua).browser.family

    @staticmethod
    def get_os(ua: str):
        return parse(ua).os.family

    @staticmethod
    def get_phone(ua: str):
        s = parse(ua).is_bot
        return parse(ua).device.family


if __name__ == '__main__':
    ua = 'Mozilla/5.0 (Linux; Android 9; VTR-AL00 Build/HUAWEIVTR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko)' \
         ' Version/4.0 Chrome/79.0.3945.116 Mobile Safari/537.36 MicroMessenger/7.0.13.1640(0x27000D39)' \
         ' Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64 WeChat/arm64'
    ua2 = "User-Agent:Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) " \
          "AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5"
    ua3 = 'User-Agent:Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50' \
          ' (KHTML, like Gecko) Version/5.1 Safari/534.50'
    ua4 = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
          " Chrome/81.0.4044.129 Safari/537.36"
    print(UAUtils.get_browser(ua))
    print(UAUtils.get_phone(ua))
    print(UAUtils.get_os(ua))
