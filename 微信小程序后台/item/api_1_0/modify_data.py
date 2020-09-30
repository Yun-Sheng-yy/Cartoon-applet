from . import api
from flask import current_app, jsonify, request
import json
from item.utils.response_code import RET
from item.models import BHistory, Collection
from item import db
from sqlalchemy.exc import IntegrityError  # 数据重复抛出的异常


@api.route("/collection_historical_data")
def collection():
    """查询保存的收藏数据"""
    # 触底加载数据，不要一次查询出所有数据
    data_type = request.args.get("type")
    # 查询不同用户的数据
    user_name = request.args.get("user_name")

    if not all([data_type, user_name]):
        return jsonify(errno=RET.NODATA, errmsg="参数不全")

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
        if data_type == "collection":
            manhuas_info = db.session.query(Collection).filter_by(user_name=user_name).slice(bg,
                                                                                             be).all()  # 查询对应的区间数据,返回的是对象哦
        elif data_type == "history":
            manhuas_info = db.session.query(BHistory).filter_by(user_name=user_name).slice(bg,
                                                                                           be).all()  # 查询对应的区间数据,返回的是对象哦
        else:
            return jsonify(errno=RET.PARAMERR, errmsg="参数有误")
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库炸了")
    if manhuas_info == []:
        return jsonify(errno=RET.NODATA, errmsg="没有更多了")

    list_li = []
    for manhua_info in manhuas_info:
        list_li.append(manhua_info.to_dict())

    json_info = json.dumps(list_li)

    return '{"errno":0, "errmsg":"OK", "data":%s }' % json_info, 200, {
        "Content-Type": "application/json"}


@api.route("/save_collection_historical", methods=["POST"])
def save_collection():
    """保存收藏数据"""
    user_data = request.get_json()
    user_name = user_data.get("user_name")
    manhua_url = user_data.get("manhua_url")
    manhua_name = user_data.get("manhua_name")
    manhua_img = user_data.get("manhua_img")
    type_data = user_data.get("type_data")
    if not all([user_name, manhua_url, type_data]):
        return jsonify(errno=RET.NODATA, errmsg="传入参数不全")

    try:
        if type_data == "save_collection":
            cb = Collection(user_name=user_name, manhua_url=manhua_url, manhua_name=manhua_name, manhua_img=manhua_img)
        elif type_data == "save_historical":
            cb = BHistory(user_name=user_name, manhua_url=manhua_url, manhua_name=manhua_name, manhua_img=manhua_img)
        else:
            return jsonify(errno=RET.PARAMERR, errmsg="参数有误")
        db.session.add(cb)
        db.session.commit()

    except IntegrityError as e:
        # 重复数据抛出的异常
        db.session.rollback()
        current_app.logger.error(e)
        if type_data == "save_collection":
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
    user_name = user_data.get("user_name")
    type_data = user_data.get("type_data")
    if not all([manhua_url, user_name, type_data]):
        return jsonify(errno=RET.NODATA, errmsg="传入参数不全")
    print("==>看看打印什么" * 20)
    print(manhua_url)
    print(user_name)
    print(type_data)
    print("==>看看打印什么" * 20)
    # 查询出数据删除掉
    try:
        # 和查询
        if type_data == "BHistory":
            user = BHistory.query.filter_by(manhua_url=manhua_url, user_name=user_name).first()
        elif type_data == "Collection":
            user = Collection.query.filter_by(manhua_url=manhua_url, user_name=user_name).first()
        # print(user)
        else:
            return jsonify(errno=RET.NODATA, errmsg="传入参数不全")
        if user is None:
            return jsonify(errno=RET.NODATA, errmsg=":)")
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="数据库错误")

    return jsonify(errno=RET.DELETE, errmsg="成功删除数据")
