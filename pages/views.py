from django.contrib.flatpages.models import FlatPage
from django.views.generic import UpdateView

from generic.views import LoginRequiredMixin, PermissionRequiredMixin
from pages.forms import FlatPageForm

class PageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = FlatPageForm
    model = FlatPage
    permission = 'flatpages.change_flatpage'
