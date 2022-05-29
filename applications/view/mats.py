from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from common.utils.rights import permission_required, view_logging_required
from models import LogModel, RoleModel, UserModel, MatModel
from . import index_bp


# 订单增加
@index_bp.get('/mat/info')
@view_logging_required
@permission_required("mat:info")
def mat_info():
    return render_template('admin/mats/mats.html')


@index_bp.get('/mat/add')
@view_logging_required
# @permission_required("admin:user:add")
def mat_add_view():
    roles = RoleModel.query.all()
    return render_template('admin/mats/mats_add.html', roles=roles)

@index_bp.get('/mat/<user_id>')
@view_logging_required
def mats_mat_id_view(user_id):
    # user = {"product_name": "圆锥", "product_num": "10", "create_at": "2022-04-13 11:49:00"}
    user = MatModel.query.get(user_id)
    return render_template('admin/mats/mats_edit.html', user=user)

# @index_bp.get('/users/center')
# @login_required
# def users_center():
#     user_logs = LogModel.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
#         desc(LogModel.create_at)).limit(10)
#     return render_template('admin/users/profile.html', user_info=current_user, user_logs=user_logs)


# @index_bp.get('/users/avatar')
# def users_avatar_view():
#     return render_template('admin/users/profile_avatar.html')
