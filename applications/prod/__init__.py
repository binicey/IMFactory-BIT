from .prods import ProdsResource, ProdResource
from flask_restful import Api

def register_prod_api(api_bp):
    prod_api = Api(api_bp, prefix='/prod')

    prod_api.add_resource(ProdsResource, '/prods')
    prod_api.add_resource(ProdResource, '/prod/<int:prod_id>')