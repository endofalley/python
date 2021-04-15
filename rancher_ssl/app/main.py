#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2021/04/15 11:24:59
@Author  :   Li Yuliang 
@Version :   1.0
@Contact :   liyl@visionarytech.com.cn
'''

# here put the import lib
import os
import sys
import docker
import datetime
import pytz
from dateutil.parser import parse
from dateutil.tz import tzutc
from apscheduler.schedulers.blocking import BlockingScheduler

def updata_ssl(container_id):
    client=docker.from_env()
    container=client.containers.get(container_id)
    # 获取证书剩余天数
    exec_result=container.exec_run("openssl x509 -in /var/lib/rancher/management-state/tls/localhost.crt -noout -enddate")
    end_time=parse(str(exec_result[1],encoding='utf-8').split('=')[1])
    now=datetime.datetime.now(tz=tzutc())
    # 证书剩余天数
    remain_day=(end_time-now).days
    # 剩余天数小于15天，更新证书
    if(remain_day<=15):
        # 备份证书
        container.exec_run("mv /var/lib/rancher/management-state/tls/localhost.crt /var/lib/rancher/management-state/tls/localhost.crt.{}".format(now.strftime("%Y%m%d%H%M%S")))
        # 更新证书
        container.restart()
def main(container_id):
    timez = pytz.timezone('Asia/Shanghai')
    scheduler=BlockingScheduler(timezone=timez)
    scheduler.add_job(func=updata_ssl,trigger="interval",days=2,next_run_time=datetime.datetime.now(),kwargs={"container_id":container_id})
    scheduler.start()

if __name__ == '__main__':
    if len(sys.argv)>1:
        container_id=sys.argv[1]
        main(container_id)
    