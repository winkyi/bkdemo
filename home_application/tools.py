# -*- coding: utf-8 -*-
from settings import APP_ID, APP_TOKEN, BK_PAAS_HOST
import requests
import json
from common.log import logger

"""
获取平台所有用户信息
"""
def get_all_user(bk_token):
    url = "%s/api/c/compapi/v2/bk_login/get_all_users/" % BK_PAAS_HOST
    form_data = {
        "app_code" : APP_ID,
        "app_secret" :APP_TOKEN,
        "bk_token" :bk_token
    }

    try:
        request = requests.get(url,form_data)
        data = json.loads(request.text)
        return data
    except Exception as e:
        logger.debug(u'get_all_user | 接口请求错误: %s' % e)
        return {}
