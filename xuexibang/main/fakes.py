#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Jinyang Shao'

'''
用于生成虚拟数据
'''

from faker import Faker
from database.models.model import UserInfo, QuestionInfo, AnswerInfo, Category, Follow
from extensions import db
import logging
import random
import click  # 在flask命令行运行时显示提示

logging.basicConfig(level=logging.DEBUG)

fake = Faker('zh_CN')


def fake_user(count=3):
    for i in range(count):
        u = UserInfo(name=fake.name(), email=fake.email(), admin=False)
        u.set_password("88888888")
        ret = db.get_result({"function":db.INSERT_USER, "content": u.to_dict()})
        click.echo(ret["content"])


def fake_category(count=5):
    ret = db.get_result({"function" : db.GET_ALL_CATEGORY})
    if ret["content"] : # 若已经建好分类
        click.echo("category already exist")
        return
    cn = ("其他", "高数", "英语", "编程", "考试")
    for i in range(count):
        category = Category(catname=cn[i])
        db.get_result({"function": db.INSERT_CATEGORY,
                       "content" : category.to_dict()})
    click.echo("category generated success!")


def fake_qna(count=10):
    for i in range(count):
        question = QuestionInfo(
            qucontent=fake.text(50),
            qutitle=fake.sentence(),
            uid=random.randint(2, 4),  # 提问者id
            qutime=fake.date_time_this_year(),
            catid=random.randint(1,5),
            ansnumber=0,   # 设置成0，之后触发器来修改
            unread=random.randint(0, 1)
        )
        ret = db.get_result({"function" : db.INSERT_QUESTION, "content" : question.to_dict()})
        click.echo(ret["success"])
    click.echo("generate %d question success" % count)

    salt = count * 2
    for i in range(salt):
        answer = AnswerInfo(
            anscontent=fake.text(30),
            anstime=fake.date_time_this_year(),
            uid=random.randint(2, 4), # 回答者id
            quid=random.randint(1, count),
            unread=random.randint(0, 1)
        )
        db.get_result({"function" : db.INSERT_ANSWER, "content":answer.to_dict()})
        # click.echo(ret)
    click.echo("generate answer success")


def fake_follow(uid=2):  # 待完成
    quid = random.randint(1, 9)
    follow = Follow(uid=uid,
                    quid=quid)
    ret = db.get_result({"function" : db.INSERT_FOLLOW, "content": follow.to_dict()})
    click.echo("generate follow uid=%d, quid=%d, %s" % (uid, quid, ret["success"]))


if __name__ == "__main__":
    fake_qna()
