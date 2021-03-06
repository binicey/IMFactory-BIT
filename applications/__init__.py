import os

from flask_cors import *
from flask import Flask, Blueprint
from common.flask_uploads import configure_uploads

from common.utils.upload import photos
from extensions import init_plugs
from applications.view import init_view
import config

api_bp: Blueprint = Blueprint('api', __name__, url_prefix='/api/v1')

from .rights import register_rights_api
from .system import register_system_api
from .users import register_users_api
from .order import register_order_api
from .mat import register_mat_api
from .prod import register_prod_api

register_rights_api(api_bp)
register_users_api(api_bp)
register_system_api(api_bp)
register_order_api(api_bp)
register_mat_api(api_bp)
register_prod_api(api_bp)

def init_api(app: Flask) -> None:
    app.register_blueprint(api_bp)


def create_app() -> Flask:
    app = Flask('智造梦想')

    #载入ico
    
    # 开启全局跨域
    CORS(app,supports_credentials=True)

    # 引入数据库配置
    app.config.from_object(config)

    # 注册各种插件
    init_plugs(app)

    # 注册路由
    init_view(app)

    # 注册接口（restful api）
    init_api(app)

    # 文件上传
    configure_uploads(app, photos)

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logo()

    return app


def logo():
    print('''
 _____                              _           _         ______ _           _    
|  __ \                    /\      | |         (_)       |  ____| |         | |   
| |__) |__  __ _ _ __     /  \   __| |_ __ ___  _ _ __   | |__  | | __ _ ___| | __
|  ___/ _ \/ _` | '__|   / /\ \ / _` | '_ ` _ \| | '_ \  |  __| | |/ _` / __| |/ /
| |  |  __/ (_| | |     / ____ \ (_| | | | | | | | | | | | |    | | (_| \__ \   < 
|_|   \___|\__,_|_|    /_/    \_\__,_|_| |_| |_|_|_| |_| |_|    |_|\__,_|___/_|\_\\

    ''')
