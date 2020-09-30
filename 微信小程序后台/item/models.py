from datetime import datetime
from . import db


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""

    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


class BHistory(BaseModel, db.Model):
    """浏览表"""
    __tablename__ = "bhistory"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    user_name = db.Column(db.String(32), nullable=False)  # 用户暱称
    manhua_url = db.Column(db.String(512), nullable=False, unique=True)  # 保存的漫画url
    manhua_name = db.Column(db.String(128))  # 保存的漫画名字
    manhua_img = db.Column(db.String(512))  # 保存的漫画图片
    is_delete = db.Column(db.Boolean(), default=False)  # 是否删除

    def to_dict(self):
        bhistoryn_info = {
            "id": self.id,
            "user_name": self.user_name,
            "manhua_url": self.manhua_url,
            "manhua_name": self.manhua_name,
            "manhua_img": self.manhua_img,
            "datatime": self.create_time.strftime("%Y-%m-%d %H:%M:%S")

        }
        return bhistoryn_info


class Collection(BaseModel, db.Model):
    """收藏表"""
    __tablename__ = "collection"
    id = db.Column(db.Integer, primary_key=True)  # 用户编号
    user_name = db.Column(db.String(32), nullable=False)  # 用户暱称
    manhua_url = db.Column(db.String(512), nullable=False, unique=True)  # 保存的漫画url
    manhua_name = db.Column(db.String(128))  # 保存的漫画名字
    manhua_img = db.Column(db.String(512))  # 保存的漫画图片
    is_delete = db.Column(db.Boolean(), default=False)  # 是否删除

    def to_dict(self):
        collection_info = {
            "id": self.id,
            "user_name": self.user_name,
            "manhua_url": self.manhua_url,
            "manhua_name": self.manhua_name,
            "manhua_img": self.manhua_img,
            "datatime": self.create_time.strftime("%Y-%m-%d %H:%M:%S")

        }
        return collection_info
