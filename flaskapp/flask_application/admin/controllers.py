from flask import Blueprint,render_template,request,redirect,url_for
from flask.ext.security import roles_required, roles_accepted
from flask_application.controllers import TemplateView
from flask.ext.mongoengine.wtf import model_form
from flask_application.posts.models import Post, Comment



admin = Blueprint('admin', __name__, url_prefix='/admin')


class AdminView(TemplateView):
    #blueprint = admin
    #route = '/'
    #route_name = 'index'
    template_name = 'admin/index.html'
    decorators = [roles_required('admin')]

    def get_context_data(self, *args, **kwargs):
        return {
            'content': 'This is the Admin Page'
        }



class AdminBlogList(TemplateView):
    #blueprint = admin
    #route = '/admin_view'
    #route_name = 'list'
    template_name = 'admin/list.html'
    decorators = [roles_required('admin')]
    cls=Post       

    def get(self):
        posts = self.cls.objects.all()
        return render_template('admin/list.html', posts=posts)

class AdminCreateNewBlog(TemplateView):
    #blueprint = admin  
    #route ="/create"
    #route_name = 'create'
    template_name = 'admin/detail.html'
    decorators = [roles_required ('admin')]
    cls=Post

    def get_context(self, slug=None):
        form_cls = model_form(Post, exclude=('created_at', 'comments'))
        if slug:
            post = Post.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, initial=post._data)
            else:
                form = form_cls(obj=post)
        else:
            post = Post()
            form = form_cls(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

        
    def get(self,slug):

        context=self.get_context(slug)
        return  render_template('admin/detail.html', **context )

    def post(self,slug):
        context =self.get_context(slug)
        form =context.get('form')

        if form.validate():
            post=context.get('post')
            form.populate_obj(post)
            post.save()
            return redirect(url_for('admin.list'))
        return render_template('admin/detail.html', **context)


class AdminBlogEditor(TemplateView):

   # blueprint = admin  
    #route ="/edit"
    #route_name = 'edit'
    #template_name = 'admin/detail.html'
    decorators = [roles_required ('admin')]
    cls=Post



    def get_context(self, slug=None):
        form_cls = model_form(Post, exclude=('created_at', 'comments'))

        if slug:
            post = Post.objects.get_or_404(slug=slug)
            if request.method == 'POST':
                form = form_cls(request.form, inital=post._data)
            else:
                form = form_cls(obj=post)
        else:
            post = Post()
            form = form_cls(request.form)

        context = {
            "post": post,
            "form": form,
            "create": slug is None
        }
        return context

    def get(self,slug):
        context = self.get_context(slug)
        return render_template('admin/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            post = context.get('post')
            form.populate_obj(post)
            post.save()

            return redirect(url_for('admin.index'))
        return render_template('admin/detail.html', **context)

    
class AdminOrEditorView(TemplateView):
    blueprint = admin
    route = '/admin/editor'
    route_name = 'admin_or_editor'
    template_name = 'admin/index.html'
    decorators = [roles_accepted('admin', 'editor')]

    def get_context_data(self, *args, **kwargs):
        return {
            'content': 'This is the Admin/Editor Page'

        }
class DeletePost(TemplateView):
    blueprint = admin
    route = '/delete'
    route_name = 'delete'
    template_name = 'admin/list.html'
    decorators = [roles_required('admin')]
    cls = Post

    def delete(self):
        try:
            post = self.cls.objects.get_or_404(post=post)
            post.delete()
        except:
            pass
        return redirect(url_for('admin.list'))

        

# http://stackoverflow.com/questions/20852184/trouble-rendering-listfield-model-form-on-mongoengine
admin.add_url_rule('/admin/', view_func=AdminView.as_view('index'))
admin.add_url_rule('/admin/list', view_func=AdminBlogList.as_view('list'))
admin.add_url_rule('/admin/create/', defaults={'slug': None}, view_func=AdminCreateNewBlog.as_view('create'))
admin.add_url_rule('/admin/<slug>/', view_func=AdminCreateNewBlog.as_view('edit'))