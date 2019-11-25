# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: global_manager.py
# 本模块包含：
# 不对外可见的数据库操作函数
from database.models.model import BaseModel
from database.models.model import UserInfo
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import InternalError


# 初始化数据库
def database_init(engine, session):
    res = {}

    try:
        # 删除所有表
        BaseModel.metadata.drop_all(engine)
        # 创建由BaseModel生成的所有表类
        BaseModel.metadata.create_all(engine)

        # 创建管理员
        admin = UserInfo(name='admin', password='123123', email='1059150030@qq.com',admin=True)

        # 插入管理员
        session.add(admin)
        session.commit()
    # 异常检测
    except Exception as e:
        print e.message
        if isinstance(e, OperationalError):
            res["success"] = False
            res["status"] = 1000
            res["message"] = e.message
            res["content"] = "Database operation fail，please check database services or operation"
            return res
        elif isinstance(e, InternalError):
            res["success"] = False
            res["status"] = 1000
            res["message"] = e.message
            res["content"] = "Database connect failed，please check database Schema's name"
            print e
            return res
        elif isinstance(e, RuntimeError):
            res["success"] = False
            res["status"] = 1000
            res["message"] = e.message
            res["content"] = "Database connect failed,please check username and password"
            return res
        else:
            res["success"] = False
            res["status"] = 1000
            res["message"] = e.message
            res["content"] = "Unknown error"
            return res

    if session.query(UserInfo).filter_by(name="admin").first() is None:
        res["success"] = False
        res["status"] = 1000
        res["message"] = "Database initiate failed,please check code"
        res["content"] = "Database initiate failed,please check code"
    else:
        res["success"] = True
        res["status"] = 0
        res["message"] = "Database initiate successfully!!!"
        res["content"] = "Database initiate successfully!!!"
    session.close()
    return res
