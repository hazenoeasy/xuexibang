# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: test.py
# 本模块为接口测试模块
from database.api.main_base import Operator

if __name__ == '__main__':
    o = Operator()


    print(u"查询admin结果:")
    print (o.get_result({"function": o.GET_UER_BY_NAME, "content": {"name": "admin"}}))

    print (u"删除admin结果:")
    print (o.get_result({"function": o.DELETE_USER_BY_NAME, "content": {"name": "admin"}}))

    print(u"查询admin结果:")
    print (o.get_result({"function": o.GET_UER_BY_NAME, "content": {"name": "admin"}}))

    print (u"插入admin结果:")
    print (o.get_result({"function": o.INSERT_USER, "content": {"name": "admin", "password": "12312313", "email": "1059150030@qq.com","admin":True}}))

    print(u"查询admin结果:")
    print (o.get_result({"function": o.GET_UER_BY_NAME, "content": {"name": "admin"}}))

    print(u"修改admin密码结果:")
    print (o.get_result({"function": o.UPDATE_USER_PWD, "content": {"name": "admin", "password": "wang"}}))

    print(u"查询admin结果:")
    print (o.get_result({"function": o.GET_UER_BY_NAME, "content": {"name": "admin"}}))

