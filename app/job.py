# -*- coding: utf-8 -*-
"""
====================================
@File Name ：job.py
@Time ： 2022/5/29 14:13
@Create by Author ： lileilei
====================================
"""
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

scheduler = BackgroundScheduler()

scheduler.add_jobstore(DjangoJobStore(),"default")
