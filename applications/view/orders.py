from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from common.utils.rights import permission_required, view_logging_required
from models import LogModel, RoleModel, UserModel, OrderModel
from . import index_bp


# 订单增加
@index_bp.get('/order/info')
@view_logging_required
@permission_required("order:info")
def order_info():
    return render_template('admin/orders/orders.html')


@index_bp.get('/order/add')
@view_logging_required
# @permission_required("admin:user:add")
def order_add_view():
    roles = RoleModel.query.all()
    return render_template('admin/orders/orders_add.html', roles=roles)

@index_bp.get('/order/<user_id>')
@view_logging_required
def orders_order_id_view(user_id):
    # user = {"product_name": "圆锥", "product_num": "10", "create_at": "2022-04-13 11:49:00"}
    user = OrderModel.query.get(user_id)
    return render_template('admin/orders/orders_edit.html', user=user)

# 订单可视化
@index_bp.get('/order/view')
@view_logging_required
@permission_required("order:view")
def order_view():
    return render_template('admin/orders/orders_view.html')

# 生产计划
@index_bp.get('/order/product')
@view_logging_required
@permission_required("product:info")
def order_count():
    return render_template('admin/orders/transport.html')

# 任务分配
@index_bp.get('/task/info')
@view_logging_required
@permission_required("task:info")
def tasks_info():
    return render_template('admin/orders/trans.html')

# @index_bp.get('/users/center')
# @login_required
# def users_center():
#     user_logs = LogModel.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
#         desc(LogModel.create_at)).limit(10)
#     return render_template('admin/users/profile.html', user_info=current_user, user_logs=user_logs)


# @index_bp.get('/users/avatar')
# def users_avatar_view():
#     return render_template('admin/users/profile_avatar.html')
