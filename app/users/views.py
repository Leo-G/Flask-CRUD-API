# resource, resources, Resources
from flask import Blueprint, request, jsonify, make_response
from app.users.models import Users, UsersSchema
from flask_restful import Resource, Api
from app.basemodels import db
from sqlalchemy.exc import SQLAlchemyError

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
        print(user_dict)
        form_errors = schema.validate(user_dict)
        if not form_errors:
            user = Users(user_dict['name'],user_dict['email'],user_dict['address'],user_dict['website'],user_dict['is_active'],user_dict['mobile'],user_dict['Birthday'])
            try:
                user.add(user)
                return jsonify({"message":"success"})            
            except SQLAlchemyError as e:
                db.session.rollback()
                reponse = make_response({"error":str(e)}, 401)              
                return reponse
                
           
        else:
            return {"errors":form_errors}

class UsersUpdate(Resource):

    def get(self, id):
        query =  Users.query.get(id)
        user = schema.dump(query).data
        return jsonify({"user":user})


    def put(self, id):
        user=Users.query.get_or_404(id)
        user_dict=request.get_json(force=True)
        form_errors = schema.validate(user_dict['user'])
        if not form_errors:
            user.name = user_dict['user']['name']            
            user.email = user_dict['user']['email']
            user.address = user_dict['user']['address']
            user.website = user_dict['user']['website']
            user.is_active = user_dict['user']['is_active']
            user.mobile = user_dict['user']['mobile']
            user.Birthday = user_dict['user']['Birthday']
            update = user.update()
            # if does not return any error
            if not update:
                  return jsonify({"message":"success"})
            else:
                  return jsonify({"message":update})

    def delete(self, id):
        user=Users.query.get_or_404(id)
        delete=user.delete(user)
        if not delete :
                 return jsonify({"message":"success"})

        else:
            return jsonify({"message":delete})
		
api.add_resource(UsersList, '/')
api.add_resource(UsersUpdate, '/<int:id>')					
