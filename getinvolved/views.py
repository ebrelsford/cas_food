from django.core.urlresolvers import reverse
from django.views.generic import CreateView, UpdateView

from forms import PostCreateForm, PostUpdateForm
from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from models import Post

class PostFormMixin(object):
    model = Post
    template_name = 'getinvolved/post_form.html'

    def get_success_url(self):
        return reverse('getinvolved_post_list')

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                     PostFormMixin, CreateView):
    form_class = PostCreateForm
    permission = 'getinvolved.create_post'

    def get_initial(self):
        initial = super(PostCreateView, self).get_initial()
        initial['added_by'] = self.request.user
        return initial

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, 
                     PostFormMixin, UpdateView):
    form_class = PostUpdateForm
    permission = 'getinvolved.change_post'

    def get_initial(self):
        initial = super(PostUpdateView, self).get_initial()
        initial['updated_by'] = self.request.user
        return initial
