# 生成报告


class GetReport:
    @staticmethod
    def get_report(arrange: dict):
        
        report = f"昨天您的站点受到 {len(arrange)} 个 IP的访问，详细情况如下：\n"
        for ip, data in arrange.items():
            report += f"{ip}: \n"
            for ua, ua_data in data.items():
                report += f"    {ua}:\n"
                for i in ua_data:
                    report += f"        {i['time_local']}: {i['request_uri']} ({i['status']}) \n"
            report += "\n"
        return report


if __name__ == '__main__':
    GetReport.get_report({})
