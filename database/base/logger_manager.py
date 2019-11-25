# -*-coding:utf-8-*-
# python: 2.7
# author: Wang Zhe
# filename: logger_manager.py
# 本模块为日志模块

import logging.handlers
import logging
import json
import time
import os


class Logger:
    def __init__(self):
        pass

    current_path = os.path.dirname(os.path.realpath(__file__))
    current_path = "/".join(current_path.split("\\")) + "/"
    with open(current_path + "../config/log_config.json") as f:
        config = f.read()
    path = json.loads(config)["log_path"]
    date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    # 生成当日日志文件路径
    log_path = "%s%s%s%s" % (path, "\\", date, ".txt")

    # 设置日志格式
    fmt = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    # 获取日志logger
    handle = logging.handlers.RotatingFileHandler(log_path)
    handle.setFormatter(fmt=fmt)

    # 初始化logger
    log = logging.getLogger()
    log.addHandler(handle)
    log.setLevel(logging.INFO)

    @classmethod
    def getpath(cls):
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        # 生成当日日志文件路径
        log_path = cls.path + "\\" + date + ".txt"
        return log_path

    @classmethod
    def info(cls, msg):
        # 检测是否需要新建日志文件
        now_path = cls.getpath()

        if now_path != cls.log_path:
            cls.handle = logging.handlers.RotatingFileHandler(now_path)
            cls.handle.setFormatter(fmt=cls.fmt)
            cls.log = logging.getLogger()
            cls.log.setLevel(logging.INFO)
            cls.log.addHandler(cls.handle)

        cls.log.info(msg)
        return

    @classmethod
    def error(cls, msg):
        now_path = cls.getpath()

        if now_path != cls.log_path:
            cls.handle = logging.handlers.RotatingFileHandler(now_path)
            cls.handle.setFormatter(fmt=cls.fmt)
            cls.log = logging.getLogger()
            cls.log.setLevel(logging.INFO)
            cls.log.addHandler(cls.handle)

        cls.log.error(msg)
        return


if __name__ == '__main__':
    Logger.error("error_test")
    Logger.info("info_test")
