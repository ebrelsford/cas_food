from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from cas_food.shortcuts import render_to_response
from schools.models import School
from forms import TrayForm

def add(request, id=None):
    initial = {
        'added_by': request.user,
        'school': get_object_or_404(School, id=id)
    }

    if request.method == 'POST':
        form = TrayForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            form.save()
            return redirect('schools.views.details', id=id)
    else:
        form = TrayForm(initial=initial)

    return render_to_response('tray/add.html', {
        'school': initial['school'],
        'form': form,
    }, context_instance=RequestContext(request))
