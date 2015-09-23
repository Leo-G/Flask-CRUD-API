# resource, resources, Resources
from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema
from flask_restful import Resource, Api
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

users = Blueprint('users', __name__, template_folder='templates')
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
#https://github.com/marshmallow-code/marshmallow-jsonapi
schema = UsersSchema(strict=True)
api = Api(users)

# Users
class UsersList(Resource):

    def get(self):
        users_query = Users.query.all()
        results = schema.dump(users_query, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        user_dict = raw_dict['data']['attributes']
        try:
                schema.validate(user_dict)
                user = Users(user_dict['name'], user_dict['email'], user_dict['address'], user_dict[
                         'website'], user_dict['is_active'], user_dict['mobile'], user_dict['Birthday'])
                user.add(user)
                query = Users.query.get(user.id)
                results = schema.dump(query).data                
                return results, 201
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 403
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 403
                return resp



class UsersUpdate(Resource):
    def get(self, id):
        user_query = Users.query.get_or_404(id)
        result = schema.dump(user_query).data
        return result

    def patch(self, id):
        user = Users.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        user_dict = raw_dict['data']['attributes']
        try:
            schema.validate(user_dict)        
            user.name = user_dict['name']
            user.email = user_dict['email']
            user.address = user_dict['address']
            user.website = user_dict['website']
            user.is_active = user_dict['is_active']
            user.mobile = user_dict['mobile']
            user.Birthday = user_dict['Birthday']
            user.update()            
            return self.get(id)
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
         

    def delete(self, id):
        user = Users.query.get_or_404(id)
        try:
            delete = user.delete(user)
            return jsonify({"message": "success"})
            
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        

api.add_resource(UsersList, '/')
api.add_resource(UsersUpdate, '/<int:id>')
