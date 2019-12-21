# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: question_manager.py
# 本模块包含：
# 不对外可见的数据库操作函数


from database.models.model import QuestionInfo


def set_question_read(quid, session):
    res = {}
    try:
        question_info = session.query(QuestionInfo).filter_by(quid=quid["quid"]).first()
        question_info.unread = False
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = ""
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


def get_unread_question(number,session):
    res = {}
    try:
        question_info_list = []
        question_list = session.query(QuestionInfo).filter_by(unread=True).limit(number["number"]).offset(number["start"]).all()
        for question in question_list:
            question_info_list.append(question.to_dict())
        res["success"] = True
        res["status"] = 0
        res["message"] = ""
        res["content"] = question_info_list
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


def get_recommend_question(number, session):
    question_info_list = []
    question_list = []
    res = {}

    try:
        question_info_list = session.query(QuestionInfo).limit(number["number"]).offset(number["start"]).all()

        for question_info in question_info_list:
            tmp = question_info.to_dict()
            question_list.append(tmp)
        res["success"] = True
        res["status"] = 0
        res["message"] = "Recommend question got"
        res["content"] = question_list
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = question_info_list
        return res


def insert_question(given, session):
    res = {}
    try:
        question_info = QuestionInfo()
        question_info.dict_init(given)
        if question_info.ansnumber is None:
            question_info.ansnumber = 0
        if question_info.unread is None:
            question_info.unread = True
        session.add(question_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "Question: %s successfully insert" % question_info.quid
        res["content"] = None
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def get_question(quid, session):
    res = {}
    try:
        question_info = session.query(QuestionInfo).filter_by(quid=quid["quid"]).first()
        if not isinstance(question_info, QuestionInfo):
            raise
        else:
            res["success"] = True
            res["status"] = 0
            res["message"] = "Question: %s successfully get" % quid["quid"]
            res["content"] = question_info.to_dict()
            return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def get_question_by_uid(uid, session):
    res = {}
    try:
        question_info_list = session.query(QuestionInfo).filter_by(uid=uid["uid"]).all()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s 'questions successfully get" % uid["uid"]
        res["content"] = []
        for question_info in question_info_list:
            res["content"].append(question_info.to_dict())

        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def delete_question_by_id(quid, session):
    res = {}
    try:
        question_info = session.query(QuestionInfo).filter_by(quid=quid["quid"]).first()
        # answer_list = session.query(AnswerInfo).filter_by(quid=quid["quid"]).all()
        # for answer in answer_list:
        # session.delete(answer)
        session.delete(question_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "Question: %s 'deleted successfully" % quid["quid"]
        res["content"] = None
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def get_question_by_cat(given, session):
    res = {}
    try:
        question_info_list = session.query(QuestionInfo).filter_by(catid=given["catid"]).limit(given["number"]).offset(
            given["start"]).all()
        question_list = []

        for question_info in question_info_list:
            question_list.append(question_info.to_dict())

        res["success"] = True
        res["status"] = 0
        res["message"] = "Category: %d 's questions got successfully" % given["catid"]
        res["content"] = question_list
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res
