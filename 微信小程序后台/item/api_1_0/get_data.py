from . import api

# import logging
from flask import current_app, jsonify, request
import json
from item.utils.response_code import RET
# 导入爬虫
from item.utils.Spiders.manhau39.manhua39_d1 import Manhau39
from item.utils.Spiders.manhau39.manhua39_d2 import manhua39detail
from item.utils.Spiders.manhau39.manhua39_d3 import ManhuaImages


@api.route("/get_title")
def get_data():
    """
     搜索漫画
    :param name 漫画名字
    :return 每漫画json数据
    """
    # 数据已经以get的方式发送过来了
    name = request.args.get("name", "")
    if not all([name]):
        return jsonify(errno=RET.NODATA, errmsg="参数为空")

    # 调用爬虫
    # 创建对象
    manhua = Manhau39(name)
    try:
        list_dict = manhua.run()
        if list_dict == []:
            return jsonify(errno=RET.NODATA, errmsg="找不到 {} 漫画:)".format(name))
        dict_json = json.dumps(dict(erron='0', errmsg="ok", data=list_dict))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="爬虫挂了")

    return dict_json, 200, {"Content-Type": "application/json"}


@api.route('/get_detail')
def get_data_detail():
    """
      接下来是漫画的详细页面
    :param 每部漫画的url
    :return 每部漫画详细话数的json数据
    """
    url = request.args.get("url", "")

    print("后端接收到请求")
    print(url)
    if not all([url]):
        return jsonify(errno=RET.NODATA, errmsg='链接为空')

    # 调用爬虫
    # 创建对象
    cmanhua = manhua39detail(url)
    try:
        list_dict = cmanhua.run()
        if list_dict == []:
            return jsonify(errno=RET.NODATA, errmsg="没有具体的章节:)")
        dict_json = json.dumps(dict(erron='0', errmsg="ok", data=list_dict))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="爬虫挂了")

    return dict_json, 200, {"Content-Type": "application/json"}


@api.route('/get_manhua_detail')
def m_detail():
    """
    :param  接收漫画每一话的url
    :return 每一话图片
    """

    url = request.args.get("url", "")

    print("后端接收到请求")
    print(url)
    if not all([url]):
        return jsonify(errno=RET.NODATA, errmsg='链接为空')

    # 调用爬虫selinum
    manhua = ManhuaImages(url)
    try:
        list_dict = manhua.run()
        if list_dict == []:
            return jsonify(errno=RET.NODATA, errmsg="图片获取失败:)")
        dict_json = json.dumps(dict(erron='0', errmsg="ok", data=list_dict))
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.THIRDERR, errmsg="爬虫挂了")

    return dict_json, 200, {"Content-Type": "application/json"}
