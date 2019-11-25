# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: question_manager.py
# 本模块包含：
# 不对外可见的数据库操作函数

from database.models.model import QuestionInfo


def get_recommend_question(number, session):
    question_list = []
    res = {}
    question_info_list = session.query(QuestionInfo).limit(number).all()

    for question_info in question_info_list:
        if isinstance(question_info, QuestionInfo):
            question_list.append(question_info.to_dict())
        else:
            res["success"] = False
            res["status"] = 1000
            res["message"] = "Unknown Error"
            res["content"] = question_info_list
            return res
    res["success"] = True
    res["status"] = 0
    res["message"] = "Recommend question got"
    res["content"] = question_info_list
    return res
