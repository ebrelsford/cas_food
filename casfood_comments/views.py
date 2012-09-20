from django.contrib.comments.models import Comment
from django.http import Http404
from django.views.generic import DeleteView

from generic.views import LoginRequiredMixin, PermissionRequiredMixin

class CommentDeleteView(DeleteView, LoginRequiredMixin, PermissionRequiredMixin):
    model = Comment
    permission = 'comments.delete_comment'

    def dispatch(self, request, *args, **kwargs):
        # confirm user can actually delete the given object
        user = request.user
        if not (user.is_superuser or self.get_object().user == user):
            raise Http404
        return super(CommentDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.commented_object = self.get_object().content_object
        return super(CommentDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return self.commented_object.get_absolute_url()
