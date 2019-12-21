# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: user_manager.py
# 本模块包含：
# 不对外可见的数据库操作函数
from database.models.model import UserInfo
from database.models.model import Follow
from database.models.model import QuestionInfo
from database.base.question_manager import delete_question_by_id


# 获取一定数量user
def get_users(number, session):
    user_info_list = []
    user_list = []
    res = {}
    try:
        user_info_list = session.query(UserInfo).limit(number["number"]).offset(number["start"]).all()

        for user_info in user_info_list:
            tmp = user_info.to_dict()
            user_list.append(tmp)
        res["success"] = True
        res["status"] = 0
        res["message"] = "Recommend question got"
        res["content"] = user_list
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = user_info_list
        return res


# 根据用户名查找用户
def get_user_by_name(user, session):
    res = {}
    try:
        user_info = session.query(UserInfo).filter_by(name=user["name"]).first()
        if user_info is None:
            raise RuntimeError("User: %s (name)not fond!" % user["name"])
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s (name) fond successfully" % user["name"]
        res["content"] = user_info.to_dict()
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None

    return res


# 根据用户id查找用户
def get_user_by_id(user, session):
    res = {}
    try:
        user_info = session.query(UserInfo).filter_by(uid=user["uid"]).first()
        if user_info is None:
            raise RuntimeError("User: %d (uid) not fond!" % user["uid"])
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %d (uid) fond successfully" % user["uid"]
        res["content"] = user_info.to_dict()
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None

    return res


# 插入新用户
def insert_user(user, session):
    res = {}

    try:
        user_info = get_user_by_name(user, session)
        user_info = UserInfo()
        user_info.dict_init(user)
        session.add(user_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s insert successfully" % user["name"]
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res

    return res


# 根据用户名删除用户
def delete_user_by_name(name, session):
    res = {}
    try:
        # 检查数据库中是否存在用户
        user_info = session.query(UserInfo).filter_by(name=name["name"]).first()

        session.delete(user_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s deleted successfully!" % name["name"]
        res["content"] = " "
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = " "

    return res


# 修改用户密码
def update_user_pwd(user, session):
    res = {}

    try:
        user_info = session.query(UserInfo).filter_by(name=user["name"]).first()
        user_info.password_hash = user["password_hash"]
        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s password update successfully!!" % user["name"]
        res["content"] = user_info.to_dict()
        session.commit()
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None

    return res


# 获取用户关注列表
def get_user_follow(user, session):
    res = {}

    try:
        user_info = session.query(UserInfo).filter_by(name=user["name"]).first()
        follow_list = []

        follow_info_list = session.query(Follow).filter_by(uid=user_info.uid).all()
        for follow_info in follow_info_list:
            question_info = session.query(QuestionInfo).filter_by(quid=follow_info.quid).first()
            follow_list.append(question_info.to_dict())

        res["success"] = True
        res["status"] = 0
        res["message"] = "User: %s's follow fond" % user["name"]
        res["content"] = follow_list
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
    return res


# 增加关注
def insert_follow(follow, session):
    res = {}
    try:
        follow_info = Follow()
        follow_info.dict_init(follow)
        session.add(follow_info)
        session.commit()

        res["success"] = True
        res["status"] = 0
        res["message"] = "Follow: %s to %s insert successfully" % (follow_info.uid, follow_info.quid)
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


# 删除关注
def delete_follow(follow, session):
    res = {}
    try:
        follow_info = session.query(Follow).filter_by(uid=follow["uid"], quid=follow["quid"]).first()
        session.delete(follow_info)
        session.commit()

        res["success"] = True
        res["status"] = 0
        res["message"] = "Follow: %s to %s deleted successfully" % (follow_info.uid, follow_info.quid)
        res["content"] = None
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res
