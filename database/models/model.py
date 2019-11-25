# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: model.py
# 本模块包含：
# ORM模型
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


# 为所有表项添加to_dict和to_json方法
class ModelProcessor:

    def __init__(self):
        pass

    def __repr__(self):
        return '{}:{}'.format(str(self.__class__), self.to_dict().__repr__())

    def to_dict(self):
        _dict = {}
        for filed in self.__get_fields():
            _dict[filed] = getattr(self, filed)
        return _dict

    def to_json(self):
        json = {}
        for col in self._sa_class_manager.mapper.mapped_table.columns:
            attr = getattr(self, col.name)
            json[col.name] = attr
        return json

    @classmethod
    def __get_fields(cls):
        return {f: getattr(cls, f).expression.type for f in cls._sa_class_manager._all_key_set}

    get_fields = __get_fields


class UserInfo(BaseModel, ModelProcessor):
    __tablename__ = "UserInfo"

    uid = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False,unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(32), nullable=False,unique=True)
    admin=Column(Boolean,nullable=True)


class QuestionInfo(BaseModel, ModelProcessor):
    __tablename__ = "QuestionInfo"

    quid = Column(Integer, primary_key=True)
    qucontent = Column(String(32), nullable=False)
    qutime = Column(DateTime, nullable=False)
    uid = Column(Integer, ForeignKey(UserInfo.uid) , nullable=False)
    ansid = Column(Integer, nullable=True)


class AnswerInfo(BaseModel, ModelProcessor):
    __tablename__ = "AnswerInfo"

    ansid = Column(Integer, primary_key=True)
    anscontent = Column(String(32), nullable=False)
    anstime = Column(DateTime, nullable=False)
    uid = Column(Integer, ForeignKey(UserInfo.uid),nullable=False)
    quid = Column(Integer, ForeignKey(QuestionInfo.uid), nullable=False)


class Follow(BaseModel, ModelProcessor):
    __tablename__ = "Follow"

    uid = Column(Integer, ForeignKey(UserInfo.uid) , nullable=False, primary_key=True)
    quid = Column(Integer, ForeignKey(QuestionInfo.uid), nullable=False, primary_key=True)
