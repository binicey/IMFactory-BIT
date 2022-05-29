from flask import request, jsonify
from flask_restful import Resource, reqparse

from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import UserModel, OrderModel

class OrdersResource(Resource):
    def get(self):
        # orders_data = [
        #     {"product_name": "圆柱", "product_num": "20", "create_at": "2022-04-13 10:49:30"},
        #     {"product_name": "圆台", "product_num": "30", "create_at": "2022-04-13 10:50:00"},
        #     {"product_name": "圆锥", "product_num": "10", "create_at": "2022-04-13 11:49:00"},
        # ]

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('product_name', type=str, default='')
        
        res = parser.parse_args()

        filters = []
        if res.product_name:
            filters.append(OrderModel.product_name.like('%' + res.product_name + '%'))

        paginate = OrderModel.query.filter(*filters).paginate(page=res.page,
                                                             per_page=res.limit,
                                                             error_out=False)
        orders_data = [{
            'id': item.id,
            'product_name': item.product_name,
            'product_num': item.product_num,
            'create_at': str(item.create_at),
        } for item in paginate.items]
        
        return table_api(result={'items': orders_data,
                                 'total': paginate.total}
                         , code=0)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", type=str)
        parser.add_argument("product_num", type=int, required=True, help="数量不能为空")
        
        res = parser.parse_args()

        order = OrderModel()
        order.product_name = res.product_name
        order.product_num = res.product_num

        db.session.add(order)
        db.session.commit()
        return success_api(message="增加成功", code=0)

class OrderResource(Resource):
        def delete(self, ord_id):
            ord = OrderModel.query.get(ord_id)
            db.session.delete(ord)
            db.session.commit()
            return success_api(message='删除成功', code=0)
        
        def put(self, ord_id):
             parser = reqparse.RequestParser()
             parser.add_argument("product_name", type=str)
             parser.add_argument("product_num", type=int, required=True, help="数量不能为空")
        
             res = parser.parse_args()

             ord = OrderModel.query.get(ord_id)

             ord.product_name = res.product_name
             ord.product_num = res.product_num
             db.session.commit()
             return success_api(message='订单修改成功', code=0)