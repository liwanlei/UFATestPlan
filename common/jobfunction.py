# -*- coding: utf-8 -*-
"""
====================================
@File Name ：jobfunction.py
@Time ： 2022/5/29 13:49
@Create by Author ： lileilei
====================================
"""
from common.config import *
from common.redisopear import RedisOpearMQ


def send(project, casetype,taskid,apkpath,tasktype,testevnt,taskname):
    '''
    给客户端推送
    '''
    redisopear = RedisOpearMQ(host=RedisHost, port=RedisPort, db=RedisDb, passwd=RedisPassword)
    msg = {"project": project, 'casetype': casetype,'id':taskid,'apkpath':apkpath,
           "tasktype":tasktype,'testvent':testevnt,'taskname':taskname}
    redisopear.publish(RedisPushChannelTotalAgent, str(msg))
