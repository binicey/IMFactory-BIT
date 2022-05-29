from .orders import OrdersResource, OrderResource
from flask_restful import Api

def register_order_api(api_bp):
    order_api = Api(api_bp, prefix='/order')

    order_api.add_resource(OrdersResource, '/orders')
    order_api.add_resource(OrderResource, '/order/<int:ord_id>')