from . import api
from flask import current_app, jsonify, request
import json
from item.utils.response_code import RET
from item.models import BHistory, Collection
from item import db
from sqlalchemy.exc import IntegrityError  # 数据重复抛出的异常


@api.route("/collection_data")
def collection():
    """查询保存的收藏数据"""
    # 触底加载数据，不要一次查询出所有数据
    bg = request.args.get("bg", "")
    be = request.args.get("be", "")
    print("后端接收到请求")

    if not all([bg, be]):
        bg = 0
        be = 20

    bg = int(bg)
    be = int(be)

    if bg > be:
        bg, be = be, bg

    try:
        collections_info = db.session.query(Collection).slice(bg, be).all()  # 查询对应的区间数据,返回的是对象哦
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库炸了")
    if collections_info == []:
        return jsonify(errno=RET.NODATA, errmsg="到底了")

    list_li = []
    for collection_info in collections_info:
        list_li.append(collection_info.to_dict())

    json_info = json.dumps(list_li)

    return '{"errno":0, "errmsg":"OK", "data":%s }' % json_info, 200, {
        "Content-Type": "application/json"}


@api.route("/historical_data")
def historical():
    """查询浏览的数据"""
    """查询保存的收藏数据"""
    # 触底加载数据，不要一次查询出所有数据
    bg = request.args.get("bg", "")
    be = request.args.get("be", "")
    print("后端接收到请求")

    if not all([bg, be]):
        bg = 0
        be = 20

    bg = int(bg)
    be = int(be)

    if bg > be:
        bg, be = be, bg

    try:
        collections_info = db.session.query(BHistory).slice(bg, be).all()  # 查询对应的区间数据,返回的是对象哦
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库炸了")
    if collections_info == []:
        return jsonify(errno=RET.NODATA, errmsg="到底了")

    list_li = []
    for collection_info in collections_info:
        list_li.append(collection_info.to_dict())

    json_info = json.dumps(list_li)

    return '{"errno":0, "errmsg":"OK", "data":%s }' % json_info, 200, {
        "Content-Type": "application/json"}


@api.route("/save_collection", methods=["POST"])
def save_collection():
    """保存收藏数据"""
    user_data = request.get_json()
    user_name = user_data.get("user_name")
    manhua_url = user_data.get("url")
    manhua_name = user_data.get("manhua_name")
    manhua_img = user_data.get("manhua_img")

    print(manhua_url)
    print(user_name)
    print(manhua_name)
    print(manhua_img)
    if not all([user_name, manhua_url]):
        return jsonify(errno=RET.NODATA, errmsg="传入参数不全")

    try:
        ct = Collection(user_name=user_name, manhua_url=manhua_url, manhua_name=manhua_name, manhua_img=manhua_img)
        db.session.add(ct)
        db.session.commit()

    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="漫画已存在数据库")

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存到数据库失败")
    return jsonify(errno=RET.OK, errmsg="成功保存到数据库")


@api.route("/save_historical", methods=["POST"])
def save_historical():
    """保存历史数据"""

    user_data = request.get_json()
    user_name = user_data.get("user_name")
    manhua_url = user_data.get("url")
    manhua_name = user_data.get("manhua_name")
    manhua_img = user_data.get("manhua_img")
    print(manhua_url)
    print(user_name)
    print(manhua_name)
    print(manhua_img)
    if not all([user_name, manhua_url]):
        return jsonify(errno=RET.NODATA, errmsg="传入参数不全")
    try:
        by = BHistory(user_name=user_name, manhua_url=manhua_url, manhua_name=manhua_name, manhua_img=manhua_img)
        db.session.add(by)
        db.session.commit()

    except IntegrityError as e:
        # 数据库操作错误后的回滚
        db.session.rollback()
        # 表示手机号出现了重复值，即手机号已注册过
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAEXIST, errmsg="漫画已存在数据库")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存到数据库失败")
    return jsonify(errno=RET.OK, errmsg="成功保存到数据库")


@api.route("/delete_data", methods=["DELETE"])
def delete_data():
    """删除浏览记录接口"""
    # 传入漫画url可以进行删除
    user_data = request.get_json()
    manhua_url = user_data.get("url")
    if not all([manhua_url]):
        return jsonify(errno=RET.NODATA, errmsg="传入参数不全")
    print(manhua_url)
    # 查询出数据删除掉
    try:
        user = BHistory.query.filter_by(manhua_url=manhua_url).first()
        # print(user)
        if user is None:
            return jsonify(errno=RET.NODATA, errmsg=":)")
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库错误")

    return jsonify(errno=RET.OK, errmsg="成功删除数据")
