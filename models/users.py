from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class UserModel(db.Model, UserMixin):
    __tablename__ = 'cp_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID')
    username = db.Column(db.String(20), comment='用户名')
    realname = db.Column(db.String(20), comment='真实名字')
    mobile = db.Column(db.String(11), comment='电话号码')
    avatar = db.Column(db.String(255), comment='头像', default="/static/admin/admin/images/avatar.jpg")
    comment = db.Column(db.String(255), comment='备注')
    password_hash = db.Column(db.String(128), comment='哈希密码')
    enable = db.Column(db.Integer, default=0, comment='启用')
    dept_id = db.Column(db.Integer, comment='部门id')

    role = db.relationship('RoleModel', secondary="rt_user_role", backref=db.backref('user'), lazy='dynamic')

    def set_password(self, password):
        """设置密码，对密码进行加密存储"""
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        """校验密码方法"""
        return check_password_hash(self.password_hash, password)

    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')


class DepartmentModel(db.Model):
    __tablename__ = 'cp_dept'
    id = db.Column(db.Integer, primary_key=True, comment="部门ID")
    parent_id = db.Column(db.Integer, comment="父级编号")
    dept_name = db.Column(db.String(50), comment="部门名称")
    leader = db.Column(db.String(50), comment="负责人")
    phone = db.Column(db.String(20), comment="联系方式")
    email = db.Column(db.String(50), comment="邮箱")
    status = db.Column(db.Boolean, comment='状态(1开启,0关闭)')
    comment = db.Column(db.Text, comment="备注")
    address = db.Column(db.String(255), comment="详细地址")
    sort = db.Column(db.Integer, comment="排序")

    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

class OrderModel(db.Model):
    __tablename__ = 'cp_order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='账号')

    product_name = db.Column(db.String(20), comment='产品名称')
    product_num = db.Column(db.Integer, default=0, comment='所需数量')

    create_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')

class MatModel(db.Model):
    __tablename__ = 'cp_mat'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='账号')
    material_name = db.Column(db.String(20), comment='物料名称')

    material_num = db.Column(db.Integer, default=0, comment='库存数量')
    model_speci = db.Column(db.String(30), comment='规格型号')
    material_mat = db.Column(db.String(30), comment='材料')

    enter_at = db.Column(db.DateTime, default=datetime.now, comment='录入时间')

class ProdModel(db.Model):
    __tablename__ = 'cp_prod'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='账号')
    product_name = db.Column(db.String(20), comment='产品名称')
    product_cate = db.Column(db.String(20), comment='产品种类')
    # proc_flow = db.Column(db.Integer, default=0, comment='加工工艺流程')
    proc_flow1 = db.Column(db.Integer, default=0, comment='工艺1')
    proc_flow2 = db.Column(db.Integer, default=0, comment='工艺2')
    proc_flow3 = db.Column(db.Integer, default=0, comment='工艺3')
    proc_flow4 = db.Column(db.Integer, default=0, comment='工艺4')
    machine1 = db.Column(db.Integer, default=0, comment='机床1')
    machine2 = db.Column(db.Integer, default=0, comment='机床2')
    machine3 = db.Column(db.Integer, default=0, comment='机床3')
    machine4 = db.Column(db.Integer, default=0, comment='机床4')
    machine5 = db.Column(db.Integer, default=0, comment='机床5')
    machine6 = db.Column(db.Integer, default=0, comment='机床6')
    machine7 = db.Column(db.Integer, default=0, comment='机床7')
    machine8 = db.Column(db.Integer, default=0, comment='机床8')
    # material_num = db.Column(db.Integer, default=0, comment='库存数量')
    # model_speci = db.Column(db.String(30), comment='规格型号')
    # material_mat = db.Column(db.String(30), comment='材料')

    enter_at = db.Column(db.DateTime, default=datetime.now, comment='录入时间')