from flask import Blueprint,render_template,request,redirect,url_for,flash

from flask_application.controllers import TemplateView , MethodView

from flask_application.posts.models import Post,Comment 
from flask.ext.mongoengine.wtf import model_form
from flask.ext.security import login_required
from flask_wtf import Form
from wtforms import StringField,TextField,validators  
from wtforms.validators import DataRequired
from pymongo.errors import OperationFailure



class PostDoc(Post):
    pass

search = Blueprint('search', __name__)

class SearchForm(Form):
    search = TextField('Search', [validators.InputRequired()])




    
class SearchListView(TemplateView):
    blueprint = search
    route = '/blogs/'
    route_name = 'search'
    template_name = 'posts/search.html'
    methods=["POST","GET"]
    # Asa per https://gitlab.com/wiliamsouza/cars/blob/master/cars/controllers.py   
    
    
    def post(self):
        results=[]
        form=SearchForm()
        query=request.form['q']
        if request.method =="POST" or "GET":        #if form.validate():
            coll=PostDoc._get_collection()
            text_results=coll.database.command("text","post",search=query,limit=10)
            doc_matches = (res['obj'] for res in text_results['results'])
            

            #flash(text_results)
               
        return render_template("posts/search2.html" ,query=query,text_results=text_results)

        
# class DetailView(TemplateView):
#     blueprint = posts
#     route = '/blogs/<slug>/'
#     route_name = 'detail'
#     template_name = 'posts/detail.html'
#     form = model_form(Comment,exclude=['created_at'])
    

#     def get_context(self,slug):
#         post =Post.objects.get_or_404(slug=slug)
#         form= self.form(request.form)

#         context ={
#             "post":post,
#             "form":form,
#         }

#         return context

#     def get(self, slug):
#         context=self.get_context(slug)
#         return render_template('posts/detail.html', **context)
#     @login_required
#     def post(self,slug):
#         context=self.get_context(slug)
#         form =context.get('form')
        

#         if form.validate():
#             comment =Comment()
#             form.populate_obj(comment)

#             post=context.get('post')
#             post.comments.append(comment)
#             post.save()

#             return redirect(url_for('posts.detail',slug=slug))

#         return render_template('posts/detail.html',**context)




#posts.add_url_rule('/blog', view_func=ListView.as_view('list'))
#posts.add_url_rule('blog/<slug>/', view_func=DetailView.as_view('detail'))