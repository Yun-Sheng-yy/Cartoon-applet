# coding:utf-8

from flask import Blueprint
from item import models


# 创建蓝图对象
api = Blueprint("api_1_0", __name__)


# 导入蓝图的视图
from . import demo, get_data, modify_data
