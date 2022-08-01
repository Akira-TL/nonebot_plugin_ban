#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :config.py
@说明    :
@时间    :2022/07/27 18:19:13
@作者    :Akira_TL
@版本    :1.0
'''


from pydantic import BaseSettings

from nonebot import get_driver
global_config = get_driver().config.dict()
class Config(BaseSettings):
    nickname = global_config['nickname']
    pass
    # Your Config Here


configs = Config()