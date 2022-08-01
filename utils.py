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

from nonebot.log import logger

def debug(text:str):
    '''
    @说明:
        对官方debug方法的扩写,将文件地址写入debug消息方便查看日志
    @返回:
        none
    '''
    logger.debug('\033[95m' + __name__[12:-6] + '\033[0m | ' + str(text))

def check_file():
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