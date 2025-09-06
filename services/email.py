import os

import yagmail

SMTP_SERVER = "smtp.feishu.cn"
SMTP_PORT = 465
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")


def send(to, subject, body):
    # 发送邮件
    yag = yagmail.SMTP(
        user=SMTP_USER,
        password=SMTP_PASSWORD,
        host=SMTP_SERVER,
        port=SMTP_PORT,
        # smtp_ssl=True,  # 若用 465 端口，开启 SSL；587 则用 smtp_starttls=True
        smtp_starttls=False
    )
    yag.send(to=to, subject=subject, contents=body)
    yag.close()

    return True
