#from marshmallow import Schema, fields, validate
from marshmallow_jsonapi import Schema, fields
from app.basemodels import db, CRUD


class Users(db.Model, CRUD):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    address = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(250), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    mobile = db.Column(db.Integer, nullable=False)
    Birthday = db.Column(db.Date, nullable=False)

    def __init__(self,  name,  email, address,  website, is_active,  mobile,  Birthday, ):

        self.name = name
        self.email = email
        self.address = address
        self.website = website
        self.is_active = is_active
        self.mobile = mobile
        self.Birthday = Birthday


class UsersSchema(Schema):

    #not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Str(dump_only=True)
    name = fields.String()
    email = fields.Email()
    address = fields.String()
    website = fields.URL()
    creation_date = fields.DateTime()
    is_active = fields.Boolean()
    mobile = fields.Integer()
    Birthday = fields.Date()
    
    #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}

    class Meta:
        type_ = 'users'
        #fields = ('id',  'name',  'email',  'address',  'website',  'creation_date',  'is_active',  'mobile',  'Birthday', )
