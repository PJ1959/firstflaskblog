import datetime
from flask import url_for
#from flask.ext.security import UserMixin, RoleMixin
from flask_application.models import db, FlaskDocument


class Post(FlaskDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    title = db.StringField(max_length=255, required=True)
    post_id= db.SequenceField(default=0)
    slug = db.StringField(max_length=255, required=True)
    body = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField('Comment'))
    
    def get_absolute_url(self):
        return url_for('post', kwargs={"slug": self.slug})

    def __unicode__(self):
        self.title
     
    meta = {
        'allow_inheritance': True,
        'indexes': [[('body', 'text'),
                     ('title', 'text'), 'slug', 'created_at']],
        'ordering': ['-created_at']
    }


class Comment(FlaskDocument):
    created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
    body = db.StringField(verbose_name="Comment", required=True)
    author = db.StringField(verbose_name="Name", max_length=255, required=True)

