#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@文件    :__init__.py
@说明    :
@时间    :2022/07/27 18:18:53
@作者    :Akira_TL
@版本    :1.0
'''

import nonebot
from tomlkit import key
from .config import configs
from .utils import *
from nonebot.params import CommandArg,RawCommand
from nonebot import on_command,get_driver, on_message
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.matcher import Matcher
import json
import re
from nonebot.adapters.onebot.v11 import (
    GROUP_ADMIN,
    GROUP_OWNER,
    Message,
    Event,
    )

debug = logger.debug
self_replay = on_message(block=False)
@self_replay.handle()
async def _(event:Event):
    if nonebot.get_bot().self_id == event.get_user_id():
        self_replay.stop_propagation(self_replay)

nickname = configs.nickname
superusers = list(get_driver().config.dict()['superusers'])
pr = 5
ban = on_command('ban',aliases=set('rm'),priority=pr,permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER,block=False)
@ban.handle()
async def _(event:Event):
    debug('jjj')
    txt = event.get_plaintext()
    cmd = txt.split(' ')[0][1:]
    if cmd in ['ban','rm']:
        ban.stop_propagation(ban)
    else:
        return
    args = txt.split(' ')[1:]
    id = re.findall('(\d+)',event.get_session_id())[0]
    check_file()
    with open('data/ban.json','r', encoding= 'utf-8') as f:
        content:dict = json.load(f)
    if id in superusers:
        id = 'all'
    init(content,id)
    # debug(type(content[id]))

    if args:
        if cmd == 'ban':
            content[id].extend(args)
            content[id] = list(set(content[id]))
        elif cmd == 'rm':
            for key in args:
                try:
                    content[id].remove(key)
                    content[id] = list(set(content[id]))
                except ValueError:
                    debug(f'不存在的值:{key}')

    else:
        if cmd == 'ban':
            content[id][0] = True
        elif cmd == 'rm':
            content[id][0] = False
    with open('data/ban.json','w', encoding= 'utf-8') as f:
        json.dump(content,f,ensure_ascii=False)
    if cmd == 'ban':
        await ban.finish('已禁用')
    elif cmd == 'rm':
        await ban.finish('已解除')

query = on_command('query_ban',aliases=set('查询禁用关键词'),rule=to_me(),priority=pr,block=True)
@query.handle()
async def _(event:Event):
    id = re.findall('(\d+)',event.get_session_id())[0]
    check_file()
    with open('data/ban.json','r', encoding= 'utf-8') as f:
        content:dict = json.load(f)
    if id in superusers:
        id = 'all'
    if content['all'][0]:
        txt = f'{nickname}已被禁用!'
    elif content[id][0]:
        txt = f'{nickname}在本群已禁用!'
    else:
        baned_keys = content[id][1:]
        if baned_keys:
            txt = '被禁用的关键词有:'
            for key in baned_keys:
                txt += '\n' + key
        else:
            txt = '当前无禁用关键词'
    await query.finish(txt)

blockf = on_message(priority=pr+1,block=False)
@blockf.handle()
async def _(event:Event,matcher:Matcher):
    txt = event.get_plaintext()
    id = re.findall('(\d+)',event.get_session_id())[0]
    check_file()
    with open('data/ban.json','r', encoding= 'utf-8') as f:
        content:dict = json.load(f)
    if content['all'][0]:
        debug('1')
        matcher.stop_propagation()
    try:
        for keyworld in content['all'][1:]:
                if keyworld in txt:
                    debug('2')
                    matcher.stop_propagation()
                    break
        if content[id][0]:
            debug('3')
            matcher.stop_propagation()
        else:
            for keyworld in content[id][1:]:
                if keyworld in txt:
                    debug('4')
                    matcher.stop_propagation()
                    break
        pass
    except KeyError:
        pass

# {'all':[true,xxx,xxx...],
# group1:[is_band_all,xxx,xxx,...],
# group2:[xxx,xxx,...]
# }
# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

