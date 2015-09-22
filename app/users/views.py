# resource, resources, Resources
from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema
from flask_restful import Resource, Api
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

users = Blueprint('users', __name__, template_folder='templates')
# http://marshmallow.readthedocs.org/en/latest/quickstart.html#declaring-schemas
schema = UsersSchema()
api = Api(users)

# Users
class UsersList(Resource):

    def get(self):
        users = Users.query.all()
        results = schema.dump(users, many=True).data
        return results

    def post(self):
        user_dict = request.get_json(force=True)            
        try:
                schema.validate(user_dict)
                user = Users(user_dict['name'], user_dict['email'], user_dict['address'], user_dict[
                         'website'], user_dict['is_active'], user_dict['mobile'], user_dict['Birthday'])
                user.add(user)
                return jsonify({"message": "success"})
            
        except ValidationError as err:
                resp = jsonify({"error": err.messages})
                resp.status_code = 401
                return resp               
                
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp



class UsersUpdate(Resource):
    def get(self, id):
        query = Users.query.get(id)
        user = schema.dump(query).data
        return jsonify({"user": user})

    def put(self, id):
        user = Users.query.get_or_404(id)
        user_dict = request.get_json(force=True)
        try:
            schema.validate(user_dict)        
            user.name = user_dict['user']['name']
            user.email = user_dict['user']['email']
            user.address = user_dict['user']['address']
            user.website = user_dict['user']['website']
            user.is_active = user_dict['user']['is_active']
            user.mobile = user_dict['user']['mobile']
            user.Birthday = user_dict['user']['Birthday']
            update = user.update()
            return jsonify({"message": "success"})
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
