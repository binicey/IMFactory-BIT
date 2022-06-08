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
            'product_cate': item.product_cate,
            # 'proc_flow': item.proc_flow,
            'proc_flow1': item.proc_flow1,
            'proc_flow2': item.proc_flow2,
            'proc_flow3': item.proc_flow3,
            'proc_flow4': item.proc_flow4,
            'machine1': item.machine1,
            'machine2': item.machine2,
            'machine3': item.machine3,
            'machine4': item.machine4,
            'machine5': item.machine5,
            'machine6': item.machine6,
            'machine7': item.machine7,
            'machine8': item.machine8,
            'enter_at': str(item.enter_at),
        } for item in paginate.items]
        
        return table_api(result={'items': prods_data,
                                 'total': paginate.total}
                         , code=0)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("product_name", type=str, required=True, help="名称不能为空")
        # parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
        parser.add_argument("product_cate", type=str)
        # parser.add_argument("proc_flow", type=int)
        parser.add_argument("proc_flow1", type=int)
        parser.add_argument("proc_flow2", type=int)
        parser.add_argument("proc_flow3", type=int)
        parser.add_argument("proc_flow4", type=int)
        parser.add_argument("machine1", type=int)
        parser.add_argument("machine2", type=int)
        parser.add_argument("machine3", type=int)
        parser.add_argument("machine4", type=int)
        parser.add_argument("machine5", type=int)
        parser.add_argument("machine6", type=int)
        parser.add_argument("machine7", type=int)
        parser.add_argument("machine8", type=int)

        res = parser.parse_args()

        prod = ProdModel()
        prod.product_name = res.product_name
        prod.product_cate = res.product_cate
        # prod.proc_flow = res.proc_flow
        prod.proc_flow1 = res.proc_flow1
        prod.proc_flow2 = res.proc_flow2
        prod.proc_flow3 = res.proc_flow3
        prod.proc_flow4 = res.proc_flow4
        prod.machine1 = res.machine1
        prod.machine2 = res.machine2
        prod.machine3 = res.machine3
        prod.machine4 = res.machine4
        prod.machine5 = res.machine5
        prod.machine6 = res.machine6
        prod.machine7 = res.machine7
        prod.machine8 = res.machine8

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
             parser.add_argument("product_cate", type=str)
            #  parser.add_argument("proc_flow", type=int)
             parser.add_argument("proc_flow1", type=int)
             parser.add_argument("proc_flow2", type=int)
             parser.add_argument("proc_flow3", type=int)
             parser.add_argument("proc_flow4", type=int)
             parser.add_argument("machine1", type=int)
             parser.add_argument("machine2", type=int)
             parser.add_argument("machine3", type=int)
             parser.add_argument("machine4", type=int)
             parser.add_argument("machine5", type=int)
             parser.add_argument("machine6", type=int)
             parser.add_argument("machine7", type=int)
             parser.add_argument("machine8", type=int)
            #  parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
            #  parser.add_argument("model_speci", type=str)
            #  parser.add_argument("material_mat", type=str)
             res = parser.parse_args()

             prod = ProdModel.query.get(prod_id)

             prod.product_name = res.product_name
             prod.product_cate = res.product_cate
            #  prod.proc_flow = res.proc_flow
             prod.proc_flow1 = res.proc_flow1
             prod.proc_flow2 = res.proc_flow2
             prod.proc_flow3 = res.proc_flow3
             prod.proc_flow4 = res.proc_flow4
             prod.machine1 = res.machine1
             prod.machine2 = res.machine2
             prod.machine3 = res.machine3
             prod.machine4 = res.machine4
             prod.machine5 = res.machine5
             prod.machine6 = res.machine6
             prod.machine7 = res.machine7
             prod.machine8 = res.machine8
            #  prod.material_num = res.material_num
            #  prod.model_speci = res.model_speci
            #  prod.material_mat = res.material_mat

             db.session.commit()
             return success_api(message='产品修改成功', code=0)