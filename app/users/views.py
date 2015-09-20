# resource, resources, Resources
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.users.models import Users, UsersSchema
from app.baseviews import add, update, delete
from flask_restful import Resource, Api

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
            add = user.add(user)
            # if does not return any error
            if not add :
                return jsonify({"message":"success"})
            else:
                return jsonify({"message":add})
        else:
            return {"errors":form_errors}

class UsersUpdate(Resource):

    def get(self, id):
        query =  Users.query.get(id)
        user = new_schema.dump(query).user_dict
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
api.add_resource(UsersUpdate, '/update')					




""""@users.route('/')
def user_index():
   


@users.route('/add', methods=['POST', 'GET'])
def user_add():
    if request.method == 'POST':
        # Validate form values by de-serializing the request,
        # http://marshmallow.readthedocs.org/en/latest/quickstart.html#validation
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:
            user = Users(
                request.form['name'],
                request.form['email'],
                request.form['password'],
                request.form['address'],
                request.form['website'],
                request.form['creation_date'],
                request.form['is_active'],
                request.form['mobile'],
                request.form['Birthday'],)
            return add(user, success_url='users.user_index', fail_url='users.user_add')
        else:
            flash(form_errors)

    return render_template('/users/add.html')


@users.route('/update/<int:id>', methods=['POST', 'GET'])
def user_update(id):
    # Get user by primary key:
    user = Users.query.get_or_404(id)
    if request.method == 'POST':
        form_errors = schema.validate(request.form.to_dict())
        if not form_errors:

            user.name = request.form['name']
            user.email = request.form['email']
            user.password = request.form['password']
            user.address = request.form['address']
            user.website = request.form['website']
            user.creation_date = request.form['creation_date']
            user.is_active = request.form['is_active']
            user.mobile = request.form['mobile']
            user.Birthday = request.form['Birthday']
            return update(user, id, success_url='users.user_index', fail_url='users.user_update')
        else:
            flash(form_errors)

    return render_template('/users/update.html', user=user)


@users.route('/delete/<int:id>', methods=['POST', 'GET'])
def user_delete(id):
    user = Users.query.get_or_404(id)
    return delete(user, fail_url='users.user_index')
"""
