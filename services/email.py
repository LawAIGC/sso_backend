import os
import logging

from alibabacloud_credentials.client import Client as CredClient
from alibabacloud_dm20151123.client import Client as DmClient
from alibabacloud_dm20151123 import models as dm_models
from alibabacloud_tea_openapi import models as open_api_models


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. 自动获取ECS实例RAM角色凭证
cred = CredClient()

# 2. 创建DirectMail客户端配置
config = open_api_models.Config(
    credential=cred,
    endpoint='dm.aliyuncs.com'
)

# 3. 初始化邮件客户端
client = DmClient(config)

from_alias = "SSO"
account_name = os.getenv("ACCOUNT_NAME", "")  # 控制台创建的发信地址


def send(to, subject, body):
    """
    使用ECS RAM角色凭证发送邮件
    确保ECS实例已附加具有DirectMail权限的RAM角色
    """
    try:
        # 4. 构建邮件请求
        request = dm_models.SingleSendMailRequest(
            account_name=account_name,
            address_type=1,
            to_address=to,
            subject=subject,
            text_body=body,
            from_alias=from_alias,
            reply_to_address=False  # 使用回信地址
        )

        # 5. 发送邮件
        response = client.single_send_mail(request)
        logger.info(f"邮件发送成功! RequestId: {response.body.request_id}")

    except Exception as e:
        logger.error(f"邮件发送失败: {str(e)}")
        return False
    else:
        return True
