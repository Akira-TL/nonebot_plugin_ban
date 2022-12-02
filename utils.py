#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :utils.py
@说明    :
@时间    :2022/07/27 18:19:17
@作者    :Akira_TL
@版本    :1.0
'''

import json
import os

from nonebot.log import logger
debug = logger.debug

def check_file():
    try:
        os.mkdir('data')
    except:
        pass
    try:
        with open('data/ban.json','r', encoding= 'utf-8') as f:pass
    except FileNotFoundError:
        with open('data/ban.json','w', encoding= 'utf-8') as f:
            json.dump({'all':[False]},f,ensure_ascii=False)

def init(content:dict,id:str):
    try:
        content[id]
    except KeyError:
        content.update({id:[False]})
    return content