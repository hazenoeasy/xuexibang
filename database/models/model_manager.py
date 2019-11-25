# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: model_manager.py
# 本模块包含：
# 创建数据库引擎，以及会话的函数
import json
import os
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

pymysql.install_as_MySQLdb()

current_path = os.path.dirname(os.path.realpath(__file__))
current_path = "/".join(current_path.split("\\")) + "/"
with open(current_path + "../config/db_config.json") as f:
    config = f.read()
    test_flag = json.loads(config)["env"]["test"]
    if test_flag == "true":
        res = json.loads(config)["mysql_test"]
    else:
        res = json.loads(config)["mysql"]
s = "%s://%s:%s@%s:%s/%s" % (
    res['db_type'], res['username'], res['pwd'], res['host'], res['port'], res['db'])
_engine = create_engine(s, poolclass=NullPool, echo=False)


# 获取数据库连接的engine
def get_engine():
    return _engine


# 创建数据库会话
def get_session():
    engine = get_engine()
    db_session = sessionmaker(bind=engine)
    _session = db_session()
    return _session


if __name__ == '__main__':
    pass
