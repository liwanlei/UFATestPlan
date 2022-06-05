# -*- coding: utf-8 -*-
"""
====================================
@File Name ：redisopear.py
@Time ： 2022/5/28 19:14
@Create by Author ： lileilei
====================================
"""

import redis
from app.models import Timmingtask,Project
def update(project,taskid,case_run):
    project_is = Project.objects.filter(name=project).first()
    print(project_is)
    if project_is is not None:
        taskid_exict = Timmingtask.objects.filter(id=int(taskid), status=False, prject=project_is).first()
    else:
        taskid_exict = Timmingtask.objects.filter(id=int(taskid), status=False).first()

    if taskid_exict.tasktyped == "一次性任务":
        taskid_exict.yunxing_status = case_run
        taskid_exict.save()

class RedisOpearMQ(object):
    def __init__(self, host, port, db, passwd):
        self.client = redis.Redis(host=host, port=port, db=db, password=passwd)

    def publish(self, channel, message):
        self.client.publish(channel=channel, message=message)

    def sub(self, channel):
        pub = self.client.pubsub()
        pub.subscribe(channel)
        msg_stream = pub.listen()
        while True:
            # 监听消息
            for msg in msg_stream:
                if msg["type"] == "message":
                    try:
                        result=eval(str(msg["data"], encoding="utf-8"))
                        project=result['project']
                        case_run=result['detail']
                        taskid=result['taskid']
                        testtyped=result['testtyped']
                        if testtyped=="task":
                            update(project,taskid,case_run)
                    except Exception as e:
                        print(e)
                        pass


if __name__ == "__main__":
    print(RedisOpearMQ("localhost", 6379, 1, None).publish("1", "22"))
    RedisOpearMQ("localhost", 6379, 1, None).sub("1")
