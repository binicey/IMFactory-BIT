from .mats import MatsResource, MatResource
from flask_restful import Api

def register_mat_api(api_bp):
    mat_api = Api(api_bp, prefix='/mat')

    mat_api.add_resource(MatsResource, '/mats')
    mat_api.add_resource(MatResource, '/mat/<int:mat_id>')