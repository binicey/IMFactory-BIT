from flask import Flask

from .index import index_bp
from .logs_view import logs_bp
from .roles import role_bp

from . import department
from . import file
from . import rights
from . import passport
from . import users
from . import orders
from . import ljt
from . import functions
from . import map
from . import mats
from . import prods

def init_view(app: Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(logs_bp)
    app.register_blueprint(role_bp)
