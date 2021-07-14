# -*- coding: utf-8 -*-
import os
import sys
import oss2

from typing import List
from alibabacloud_sts20150401.client import Client as Sts20150401Client
from alibabacloud_sts20150401.models import AssumeRoleResponse
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_sts20150401 import models as sts_20150401_models
from analysis.conf.yconfig import YConfig


# https://next.api.aliyun.com/api/Sts/2015-04-01/AssumeRole?spm=a2c4g.11186623.2.11.259a7fedrfwTfw&params={}
class AliyunOss:
    def __init__(self):
        pass

    @staticmethod
    def create_client(
        access_key_id: str,
        access_key_secret: str,
    ) -> Sts20150401Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的AccessKey ID,
            access_key_id=access_key_id,
            # 您的AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = YConfig.get('oss:sts:endpoint')
        return Sts20150401Client(config)

    @staticmethod
    def get_sts_access_credential(
        args: List[str],
    ) -> AssumeRoleResponse:
        client = AliyunOss.create_client(YConfig.get('oss:sts:access_key_id'), YConfig.get('oss:sts:access_key_secret'))
        assume_role_request = sts_20150401_models.AssumeRoleRequest(
            duration_seconds=3600,
            role_arn=YConfig.get('oss:sts:role_arn'),
            role_session_name='fund_assistance_session'
        )
        response = client.assume_role(assume_role_request)
        print(response.body)
        return response

    @staticmethod
    async def get_sts_access_credential_async(
        args: List[str],
    ) -> AssumeRoleResponse:
        client = AliyunOss.create_client(YConfig.get('oss:sts:access_key_id'), YConfig.get('oss:sts:access_key_secret'))
        assume_role_request = sts_20150401_models.AssumeRoleRequest(
            duration_seconds=3600,
            role_arn=YConfig.get('oss:sts:role_arn'),
            role_session_name='fund_assistance_session'
        )
        response = await client.assume_role_async(assume_role_request)
        print(response.body)
        return response

    @staticmethod
    def put_object(file: str, local_file: str):
        """
        OSS上传文件
        @param file OSS object path
        @param local_file local file full path
        @return PutObjectResult
        """
        auth = oss2.Auth(YConfig.get('oss:ram:access_key_id'), YConfig.get('oss:ram:access_key_secret'))
        bucket = oss2.Bucket(auth, YConfig.get('oss:ram:endpoint'), 'cirno-fund-assistance')
        put_object_result = bucket.put_object_from_file(file, local_file)
        return put_object_result

    @staticmethod
    def put_objects(oss_path: str, local_files: list):
        for file in local_files:
            AliyunOss.put_object(oss_path + os.path.split(file)[1], file)


if __name__ == '__main__':
    AliyunOss.get_sts_access_credential(sys.argv[1:])
