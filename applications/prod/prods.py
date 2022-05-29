from flask import request, jsonify
from flask_restful import Resource, reqparse

from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import UserModel, ProdModel

class ProdsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('product_name', type=str, default='')
        
        res = parser.parse_args()

        filters = []
        if res.product_name:
            filters.append(ProdModel.product_name.like('%' + res.product_name + '%'))

        paginate = ProdModel.query.filter(*filters).paginate(page=res.page,
                                                             per_page=res.limit,
                                                             error_out=False)
        prods_data = [{
            'id': item.id,
            'product_name': item.product_name,
            # 'material_num': item.material_num,
            # 'model_speci': item.model_speci,
            # 'material_mat': item.material_mat,
            'enter_at': str(item.enter_at),
        } for item in paginate.items]
        
        return table_api(result={'items': prods_data,
                                 'total': paginate.total}
                         , code=0)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", type=str)
        # parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
        # parser.add_argument("model_speci", type=str)
        # parser.add_argument("material_mat", type=str)

        res = parser.parse_args()

        prod = ProdModel()
        prod.product_name = res.product_name
        # prod.material_num = res.material_num
        # prod.model_speci = res.model_speci
        # prod.material_mat = res.material_mat

        db.session.add(prod)
        db.session.commit()
        return success_api(message="增加成功", code=0)

class ProdResource(Resource):
        def delete(self, prod_id):
            prod = ProdModel.query.get(prod_id)
            db.session.delete(prod)
            db.session.commit()
            return success_api(message='删除成功', code=0)
        
        def put(self, prod_id):
             parser = reqparse.RequestParser()
             parser.add_argument("product_name", type=str)
            #  parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
            #  parser.add_argument("model_speci", type=str)
            #  parser.add_argument("material_mat", type=str)
             res = parser.parse_args()

             prod = ProdModel.query.get(prod_id)

             prod.product_name = res.product_name
            #  prod.material_num = res.material_num
            #  prod.model_speci = res.model_speci
            #  prod.material_mat = res.material_mat

             db.session.commit()
             return success_api(message='产品修改成功', code=0)