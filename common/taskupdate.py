# -*- coding: utf-8 -*-
"""
====================================
@File Name ：taskupdate.py
@Time ： 2022/5/29 15:39
@Create by Author ： lileilei
====================================
"""

from common.redisopear import RedisOpearMQ
from common.config import *

def RedisTaskOpear():
    RedisOpearMQ(RedisHost, RedisPort, RedisDb, RedisPassword).sub(RedisPushChannelTotalPlan)
