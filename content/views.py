from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext

from cas_food.shortcuts import render_to_response
from schools.models import School
from forms import NoteForm, PictureForm, VideoForm

@permission_required('content.add_note')
def add_note(request, id=None):
    return _add(request, id, NoteForm, 'Note')

@permission_required('content.add_picture')
def add_picture(request, id=None):
    return _add(request, id, PictureForm, 'Picture', is_multipart=True)

@permission_required('content.add_video')
def add_video(request, id=None):
    return _add(request, id, VideoForm, 'Video')

def _add(request, school_id, form_class, type_text, is_multipart=False):
    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':
        if is_multipart:
            form = form_class(request.POST, request.FILES) 
        else:
            form = form_class(request.POST) 
        if form.is_valid():    
            form.save()        
            return redirect('schools.views.details', id=school_id)
    else:
        form = form_class(initial={
            'school': school,        
            'added_by': request.user,
        })

    return render_to_response('content/add.html', {
        'type': type_text,
        'school': school,
        'form': form,
        'is_multipart': is_multipart,
    }, context_instance=RequestContext(request))
