# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: main_base.py
# 本模块包含：
# 将数据库包装为对外安全易用的接口类Operator
# 控制数据库进行操作的若干常量

from database.models.model_manager import get_session
from database.models.model_manager import get_engine
from database.base.global_manager import *
from database.base.user_manager import *
from database.base.logger_manager import *


# 建立数据库引擎
engine = get_engine()


class Operator:

    def __init__(self):
        # 初始化数据库
        self.DATABASE_INIT = 0

        # 根据用户名获取用户信息
        self.GET_UER_BY_NAME = 1

        # 插入用户
        self.INSERT_USER = 2

        # 根据用户名删除用户
        self.DELETE_USER_BY_NAME = 3

        # 根据用户名更新密码
        self.UPDATE_USER_PWD = 4

        # 获取推荐问题列表
        self.GET_RECOMMEND_QUESTION = 5

        # 获取用户关注的问题列表
        self.GET_USER_FOLLOW = 6

    def get_result(self, given):
        """
        数据库操作函数
        :param given:一个dict对象，参数为
                'function':操作数，指定数据库操作行为
                'content':数据库操作所需数据（若有）
        :return: 一个dict对象，参数为
                'success'：数据库操作是否成功
                'message':传送的信息
                'content':从数据库获取的数据（若没有则为NONE）
                'status':此次操作状态（暂未完善）
        :raises:None
        """
        session = get_session()
        function = given.get("function")
        cont = given.get("content")
        dev = given.get("dev")
        res = {}
        if function == self.DATABASE_INIT and dev is True:
            res = database_init(engine=engine, session=session)
        elif function == self.GET_UER_BY_NAME:
            res = get_user_by_name(cont, session)
        elif function == self.INSERT_USER:
            res = insert_user(cont, session)
        elif function == self.DELETE_USER_BY_NAME:
            res = delete_user_by_name(cont, session)
        elif function == self.UPDATE_USER_PWD:
            res = update_user_pwd(cont, session)

        session.close()
        if res["success"] is True:
            Logger.info(res["message"])
        else:
            Logger.error(res["message"])
        return res


if __name__ == '__main__':
    Logger.info("test")
