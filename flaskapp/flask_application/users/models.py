from flask.ext.security import UserMixin, RoleMixin

from flask_application.models import db, FlaskDocument

import datetime


class Role(FlaskDocument, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(FlaskDocument, UserMixin):
    email = db.StringField(max_length=255)
    username = db.StringField(max_length=255)
    password = db.StringField(max_length=255)
    active = db.BooleanField(default=True)
    first_name=db.StringField(max_length=255)
    last_name=db.StringField(max_length=255)
    roles = db.ListField(db.ReferenceField(Role), default=[])
    created_at = db.DateTimeField(default=datetime.datetime.now,)
    user_id=db.SequenceField(required=True,default=0)
     
    #email confirmation
    confirmed_at = db.DateTimeField()
    #tracking
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField()
    current_login_ip = db.StringField()
    login_count = db.IntField()

    #def __unicode__(self):
        #return '%s' % self.id

    #def __repr__(self):
       # return "%s %s %s" % (self.username, self.id, self.email)


   #def get_id(self):
       # return unicode(self.id)

    #meta = {
       # 'allow_inheritance': True,
       # 'indexes': ['-created_at', 'email', 'username',],
       # 'ordering': ['-created_at'],
       # 'index_drop_dups': True,

    #}


    

