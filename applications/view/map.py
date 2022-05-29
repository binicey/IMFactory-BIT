from flask import render_template
from flask_login import login_required, current_user
from sqlalchemy import desc

from common.utils.rights import permission_required, view_logging_required
from models import LogModel, RoleModel, UserModel
from . import index_bp


# 地图
@index_bp.get('/map/info')
@view_logging_required
@permission_required("map:info")
def map_info():
    return render_template('admin/map/map.html')