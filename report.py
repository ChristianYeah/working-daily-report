# -*- coding: utf-8 -*-
from invoke import run
import os
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pymongo import MongoClient
import random
import argparse
import config

if config.MONGO_USE_REPLICASET:
    client = MongoClient(config.MONGO_URL, replicaSet=config.MONGO_REPLICA_SET)
else:
    client = MongoClient(config.MONGO_URL)

db = client[config.MONGO_DB]

# 日报
EMAIL_MESSAGE = """
Dear:<br />
<strong>今天:</strong><br />
"""


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", type=str, help=u'明日工作计划, 半角逗号分隔')
    parser.add_argument("-n", type=int, help=u'抽取之前工作提交的数量, 默认单个项目随机1-3', default="3")
    parser.add_argument("-f", help=u'强制单个项目随机n条', default="0")
    parser.add_argument("--previous", help=u'抽取之前的工作内容', action="store_true")
    args = parser.parse_args()
    forces = []
    if args.f != "0":
        forces = str(args.f).split(",")
        try:
            forces = [int(f) for f in forces]
        except ValueError:
            forces = [5]
        if len(config.WORKING_DIRS) > len(forces):
            forces += forces[0] * (len(config.WORKING_DIRS) - len(forces))
        else:
            forces = forces[:len(config.WORKING_DIRS)]
    project_messages = {}
    for project_name, project_path in config.WORKING_DIRS.items():
        with cd(project_path):
            out = run("git log --pretty=format:\"%ai{AKC}%ae{AKC}%s\"", hide='both')
            commits = str(out.stdout).split("\n")
            messages = previous = {}
            for commit in commits:
                commit_time, commit_author, commit_message = commit.split("{AKC}")
                if datetime.strptime(commit_time, "%Y-%m-%d %H:%M:%S %z").strftime(
                        "%Y-%m-%d") == datetime.now().strftime("%Y-%m-%d") and commit_author == config.AUTHOR_EMAIL:
                    messages[commit_message] = commit_message
                elif args.previous is True:
                    if len(previous) < random.randint(1, args.n) or \
                            len(previous) < forces[list(config.WORKING_DIRS).index(project_name)]:
                        previous[commit_message] = commit_message

            project_messages[project_name] = [key for key in messages.keys()]
            project_messages[project_name] += [key for key in previous.keys()]
    server = smtplib.SMTP_SSL(host=config.SMTP_HOST, port=config.SMTP_PORT)
    msg = MIMEMultipart()
    msg['From'] = config.MAIL_FROM
    msg['To'] = config.MAIL_TO
    msg['Subject'] = "日报-{0}-{1}-{2}-{3}".format(config.DEPARTMENT, config.POSITION, config.NAME,
                                                 datetime.now().strftime("%Y%m%d"))

    index = 1
    daily_works = {}
    for project_name, works in project_messages.items():
        daily_works[project_name] = project_name
        EMAIL_MESSAGE += "{0}、{1}<br />".format(index, config.WORKING_PLATFORMS_NAMES[project_name])
        for work_index in range(len(works)):
            EMAIL_MESSAGE += "{0}{1}.{1}、{2}<br />".format("&nbsp;" * 4, index, work_index + 1,
                                                           works[work_index])
        index += 1

    EMAIL_MESSAGE += "<strong>明天:</strong><br />"

    index = 1
    for platform in daily_works.keys():
        tomorrow_works = [tomorrow_work for tomorrow_work in db.qiangdeerpi.find({"platform": platform})]
        if len(daily_works) > 0:
            EMAIL_MESSAGE += "{0}、{1}<br />".format(index, config.WORKING_PLATFORMS_NAMES[platform])
            work_index = 1
            for work_index in range(len(tomorrow_works)):
                EMAIL_MESSAGE += "{0}{1}.{1}、{2}<br />".format("&nbsp;" * 4, index, work_index + 1,
                                                               tomorrow_works[work_index][
                                                                   "message"])
            index += 1

    if args.t is not None:
        plans = str(args.t).split(',')
        for plan in plans:
            EMAIL_MESSAGE += "{0}、{1}<br />".format(index, plan)
            index += 1
    if config.BITCHING is True:
        EMAIL_MESSAGE += "<strong>鸡汤:</strong><br />"
        documents = [document["message"] for document in db.qiangdeyipi.find()]
        EMAIL_MESSAGE += documents[random.randint(0, len(documents) - 1)]

    msg.attach(MIMEText(EMAIL_MESSAGE, 'html', 'utf-8'))
    server.login(config.MAIL_FROM, config.MAIL_PASS)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print("OK")
