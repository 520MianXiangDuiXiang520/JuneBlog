from email.mime.text import MIMEText
import Setting
import smtplib
import datetime


class EmailUtil:
    @staticmethod
    def send(content: str,
             subject: str = f'{(datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")}'
                            f'站点访问情况汇总'):
        content = MIMEText(content, 'plain', 'utf-8')
        content['To'] = Setting.TO_EMAIL
        content['From'] = Setting.FROM_EMAIL
        content['Subject'] = subject
        smtp_server = smtplib.SMTP_SSL(Setting.SMTP_SERVER, 465)
        smtp_server.login(Setting.FROM_EMAIL, Setting.SMTP_AUTO)
        smtp_server.sendmail(Setting.FROM_EMAIL, [Setting.TO_EMAIL], content.as_string())
        smtp_server.quit()
        

if __name__ == '__main__':
    EmailUtil.send("hello email")
