# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: category_manager.py

from database.models.model import Category


def insert_category(category, session):
    res = {}
    try:
        category_info = Category()
        category_info.dict_init(category)
        session.add(category_info)
        session.commit()
        res["success"] = True
        res["status"] = 0
        res["message"] = "Category: id: %d  name: %s insert successfully" % (category_info.catid, category_info.catname)
        res["content"] = None
        return res
    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res

def delete_category(id, session):
    res = {}
    try:
        category_info = session.query(Category).filter_by(catid=id["catid"]).first()
        session.delete(category_info)
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


def get_all_category(session):
    res = {}
    try:
        category_info_list = session.query(Category).all()
        category_dict={}
        for category_info in category_info_list:
            category_dict[category_info.catid] = category_info.catname

        res["success"] = True
        res["status"] = 0
        res["message"] = "Category info got successfully"
        res["content"] = category_dict
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res


def get_cat_by_name(name, session):
    res = {}
    try:
        cat = session.query(Category).filter_by(catname = name["catname"]).first()
        res["success"] = True
        res["status"] = 0
        res["message"] = ""
        res["content"] = cat.to_dict()
        return res

    except Exception as e:
        res["success"] = False
        res["status"] = 1000
        res["message"] = e.message
        res["content"] = None
        return res

def tmp():
    res = {}
    try:
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
