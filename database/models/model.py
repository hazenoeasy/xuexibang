# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: model.py
# 本模块包含：
# ORM模型

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from database.models.model_manager import get_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import event

from werkzeug.security import generate_password_hash, check_password_hash  # 用于密码hash

from flask_login import UserMixin

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

    def dict_init(self, dict):
        for filed in self.__get_fields():
            setattr(self, filed, dict.get(filed))

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


class Category(BaseModel, ModelProcessor):
    __tablename__ = "Category"

    catid = Column(Integer, nullable=False, primary_key=True)
    catname = Column(String(32), nullable=False, unique=True)
    __table_args__ = {
        'mysql_charset': 'UTF8MB4'
    }


class UserInfo(BaseModel, ModelProcessor, UserMixin):
    __tablename__ = "UserInfo"

    uid = Column(Integer, primary_key=True)

    name = Column(String(32), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(32), nullable=False, unique=True)
    admin = Column(Boolean, nullable=True)
    __table_args__ = {

        'mysql_charset': 'UTF8MB4'

    }

    def get_id(self):
        return self.uid

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class QuestionInfo(BaseModel, ModelProcessor):
    __tablename__ = "QuestionInfo"

    quid = Column(Integer, primary_key=True)
    qucontent = Column(String(128), nullable=False)

    qutitle = Column(String(32), nullable=False)
    qutime = Column(DateTime, nullable=False)
    uid = Column(Integer, ForeignKey(UserInfo.uid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    ansid = Column(Integer, nullable=True)
    catid = Column(Integer, ForeignKey(Category.catid, onupdate="CASCADE"), nullable=True)
    ansnumber = Column(Integer, nullable=False)

    unread = Column(Boolean, nullable=False)

    __table_args__ = {

        'mysql_charset': 'UTF8MB4'

    }


class AnswerInfo(BaseModel, ModelProcessor):
    __tablename__ = "AnswerInfo"

    ansid = Column(Integer, primary_key=True)
    anscontent = Column(String(128), nullable=False)
    anstime = Column(DateTime, nullable=False)

    uid = Column(Integer, ForeignKey(UserInfo.uid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    quid = Column(Integer, ForeignKey(QuestionInfo.quid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False)

    unread = Column(Boolean, nullable=False)

    __table_args__ = {

        'mysql_charset': 'UTF8MB4'

    }


class Follow(BaseModel, ModelProcessor):
    __tablename__ = "Follow"

    uid = Column(Integer, ForeignKey(UserInfo.uid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False,
                 primary_key=True)
    quid = Column(Integer, ForeignKey(QuestionInfo.quid, ondelete="CASCADE", onupdate="CASCADE"), nullable=False,
                  primary_key=True)

    __table_args__ = {
        'mysql_charset': 'UTF8MB4'
    }


class Tmp:
    def __init__(self, dict):
        for key in dict:
            setattr(Tmp, key, dict.get(key))
