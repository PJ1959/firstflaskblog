from flask import Blueprint,render_template,request,redirect,url_for

from flask.ext.security import login_required

from flask_application.controllers import TemplateView

from wtforms import Form, BooleanField, TextField, validators
from flask_application.users.models import User



class RegistrationForm(Form):
    username     = TextField('Username', [validators.Length(min=4, max=25)])
    email        = TextField('Email Address', [validators.Length(min=6, max=35)])
    #accept_rules = BooleanField('I accept the site rules', [validators.Required()])

class ProfileForm(Form):
    #birthday  = DateTimeField('Your Birthday', format='%m/%d/%y')
    #signature = TextAreaField('Forum Signature')
    pass
class AdminProfileForm(ProfileForm):
    username = TextField('Username', [validators.Length(max=40)])
    #level    = IntegerField('User Level', [validators.NumberRange(min=0, max=10)])



users = Blueprint('users', __name__)


class ProfileView(TemplateView):
    blueprint = users
    route = '/profile'
    route_name = 'profile'
    template_name = 'profiles/profile.html'
    decorators = [login_required]

    
    def get(self):      

        
        users = User.objects.all()
        
        return render_template('profiles/profile.html', users=users)
