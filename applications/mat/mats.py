from flask import request, jsonify
from flask_restful import Resource, reqparse

from common.utils.http import fail_api, success_api, table_api
from extensions import db
from models import UserModel, MatModel

class MatsResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('limit', type=int, default=10)
        parser.add_argument('material_name', type=str, default='')
        
        res = parser.parse_args()

        filters = []
        if res.material_name:
            filters.append(MatModel.material_name.like('%' + res.material_name + '%'))

        paginate = MatModel.query.filter(*filters).paginate(page=res.page,
                                                             per_page=res.limit,
                                                             error_out=False)
        mats_data = [{
            'id': item.id,
            'material_name': item.material_name,
            'material_num': item.material_num,
            'model_speci': item.model_speci,
            'material_mat': item.material_mat,
            'enter_at': str(item.enter_at),
        } for item in paginate.items]
        
        return table_api(result={'items': mats_data,
                                 'total': paginate.total}
                         , code=0)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("material_name", type=str)
        parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
        parser.add_argument("model_speci", type=str)
        parser.add_argument("material_mat", type=str)

        res = parser.parse_args()

        mat = MatModel()
        mat.material_name = res.material_name
        mat.material_num = res.material_num
        mat.model_speci = res.model_speci
        mat.material_mat = res.material_mat

        db.session.add(mat)
        db.session.commit()
        return success_api(message="增加成功", code=0)

class MatResource(Resource):
        def delete(self, mat_id):
            mat = MatModel.query.get(mat_id)
            db.session.delete(mat)
            db.session.commit()
            return success_api(message='删除成功', code=0)
        
        def put(self, mat_id):
             parser = reqparse.RequestParser()
             parser.add_argument("material_name", type=str)
             parser.add_argument("material_num", type=int, required=True, help="数量不能为空")
             parser.add_argument("model_speci", type=str)
             parser.add_argument("material_mat", type=str)
             res = parser.parse_args()

             mat = MatModel.query.get(mat_id)

             mat.material_name = res.material_name
             mat.material_num = res.material_num
             mat.model_speci = res.model_speci
             mat.material_mat = res.material_mat

             db.session.commit()
             return success_api(message='订单修改成功', code=0)