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
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""
    def get(self):
        users_query = Users.query.all()
        results = schema.dump(users_query, many=True).data
        return results
    
    """http://jsonapi.org/format/#crud
    A resource can be created by sending a POST request to a URL that represents a collection of resources. The request MUST include a single resource object as primary data. The resource object MUST contain at least a type member.
    If a POST request did not include a Client-Generated ID and the requested resource has been created successfully, the server MUST return a 201 Created status code"""
    
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
    
    """http://jsonapi.org/format/#fetching
    A server MUST respond to a successful request to fetch an individual resource or resource collection with a 200 OK response.
    A server MUST respond with 404 Not Found when processing a request to fetch a single resource that does not exist, except when the request warrants a 200 OK response with null as the primary data (as described above)
    a self link as part of the top-level links object"""
    
    def get(self, id):
        user_query = Users.query.get_or_404(id)
        result = schema.dump(user_query).data
        return result
        
    """http://jsonapi.org/format/#crud-updating
    The PATCH request MUST include a single resource object as primary data. The resource object MUST contain type and id members.
    If a request does not include all of the attributes for a resource, the server MUST interpret the missing attributes as if they were included with their current values. The server MUST NOT interpret missing attributes as null values.
    If a server accepts an update but also changes the resource(s) in ways other than those specified by the request (for example, updating the updated-at attribute or a computed sha), it MUST return a 200 OK response. The response document MUST include a representation of the updated resource(s) as if a GET request was made to the request URL.
    A server MUST return 404 Not Found when processing a request to modify a resource that does not exist."""
    
    def patch(self, id):
        user = Users.query.get_or_404(id)
        raw_dict = request.get_json(force=True)
        user_dict = raw_dict['data']['attributes']
        try:
            for key, value in user_dict.items():
                schema.validate({key:value})
                setattr(user, key, value)
          
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
         
    #http://jsonapi.org/format/#crud-deleting
    #A server MUST return a 204 No Content status code if a deletion request is successful and no content is returned.
    def delete(self, id):
        user = Users.query.get_or_404(id)
        try:
            delete = user.delete(user)
            return 204
            
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                resp.status_code = 401
                return resp
        

api.add_resource(UsersList, '/')
api.add_resource(UsersUpdate, '/<int:id>')
