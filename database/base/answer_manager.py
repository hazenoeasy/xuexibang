# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: answer_manager.py
from database.models.model import AnswerInfo


def set_answer_read(ansid, session):
    res = {}
    try:
        answer_info = session.query(AnswerInfo).filter_by(ansid=ansid["ansid"]).first()
        answer_info.unread = False
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


def get_unread_answer(number, session):
    res = {}
    try:
        answer_info_list = []
        answer_list = session.query(AnswerInfo).filter_by(unread=True).limit(number["number"]).offset(number["start"]).all()
        for answer in answer_list:
            answer_info_list.append(answer.to_dict())
        res["success"] = True
        res["status"] = 0
        res["message"] = ""
        res["content"] = answer_info_list
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


def insert_answer(answer, session):
    res = {}
    try:
        answer_info = AnswerInfo()
        answer_info.dict_init(answer)
        session.add(answer_info)
        session.commit()

        res["success"] = True
        res["status"] = 0
        res["message"] = "Answer: %s insert successfully" % answer_info.ansid
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


def get_answer_by_id(ansid, session):
    res = {}
    try:
        answer_info = session.query(AnswerInfo).filter_by(ansid=ansid["ansid"]).first()
        if not isinstance(answer_info, AnswerInfo):
            raise
        else:
            res["success"] = True
            res["status"] = 0
            res["message"] = "Question: %s successfully get" % answer_info.ansid
            res["content"] = answer_info.to_dict()
            return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def get_answer_by_quid(quid, session):
    res = {}
    try:
        answer_info_list = session.query(AnswerInfo).filter_by(unread=False).filter_by(quid=quid["quid"]).all()
        res["success"] = True
        res["status"] = 0
        res["message"] = "Question: %s 'answers successfully get" % quid["quid"]
        res["content"] = []
        for answer_info in answer_info_list:
            res["content"].append(answer_info.to_dict())

        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def get_answer_by_uid(uid, session):
    res = {}
    try:
        answer_info_list = session.query(AnswerInfo).filter_by(uid=uid["uid"]).all()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s 'answers successfully get" % uid["uid"]
        res["content"] = []
        for answer_info in answer_info_list:
            res["content"].append(answer_info.to_dict())

        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res


def delete_answer_by_id(ansid, session):
    res = {}
    try:
        answer_info = session.query(AnswerInfo).filter_by(ansid=ansid["ansid"]).first()
        res["success"] = True
        res["status"] = 0
        res["message"] = "Answer: %s 'deleted successfully" % ansid["ansid"]
        res["content"] = None
        session.delete(answer_info)
        session.commit()
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1002
        res["message"] = e.message
        res["content"] = None
        return res
