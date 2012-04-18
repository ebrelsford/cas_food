from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext

from forms import AddEntryForm, ChangeEntryForm
from models import Entry

@permission_required('glossary.add_entry')
def create(request):
    if request.method == 'POST':
        form = AddEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('glossary_list')
    else:
        form = AddEntryForm(initial={'added_by': request.user})
    return render_to_response('glossary/entry_form.html', {
        'form': form,
    }, context_instance=RequestContext(request))

@permission_required('glossary.change_entry')
def update(request, slug):
    entry = get_object_or_404(Entry, slug=slug)
    if request.method == 'POST':
        form = ChangeEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('glossary_list')
    else:
        form = ChangeEntryForm(instance=entry,
                               initial={ 'updated_by': request.user, })
    return render_to_response('glossary/entry_form.html', {
        'form': form,
    }, context_instance=RequestContext(request))
