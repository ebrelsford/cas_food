import json

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from organize.models import Organizer
from schools.models import School
from forms import PasswordResetForm
from models import UserProfile

@csrf_protect
def password_reset(request, email=None, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.txt',
                   html_email_template_name='registration/password_reset_email.html',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None):
    if post_reset_redirect is None:
        post_reset_redirect = reverse('django.contrib.auth.views.password_reset_done')
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {}
            opts['use_https'] = request.is_secure()
            opts['token_generator'] = token_generator
            opts['email_template_name'] = email_template_name
            opts['html_email_template_name'] = html_email_template_name
            opts['request'] = request
            if is_admin_site:
                opts['domain_override'] = request.META['HTTP_HOST']
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form(initial={
            'email': email,
        })
    return render_to_response(template_name, {
        'form': form,
    }, context_instance=RequestContext(request))

@permission_required('accounts.can_follow_schools')
def follow(request, school_slug):
    """Start following a school"""
    status = 'OK'
    try:
        school = School.objects.get(slug=school_slug)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.schools_following.add(school)
        user_profile.save()
    except:
        status = 'failure'

    return HttpResponse(json.dumps({ 'status': status }),
                        mimetype='application/json')            

@permission_required('accounts.can_follow_schools')
def unfollow(request, school_slug):
    """Stop following a school"""
    status = 'OK'
    try:
        school = School.objects.get(slug=school_slug)
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.schools_following.remove(school)
        user_profile.save()
    except:
        status = 'failure'

    return HttpResponse(json.dumps({ 'status': status }),
                        mimetype='application/json')            

@login_required
def user_schools(request):
    schools = _user_watched_schools(request.user) + _user_organized_schools(request.user)
    schools = sorted(list(set(schools)), key=lambda s: s.name)

    # if user following one school, redirect there
    if len(schools) == 1:
        return redirect('schools.views.details', school_slug=schools[0].slug)

    # else, show all schools, let user choose
    return render_to_response('accounts/user_schools.html', {
        'schools': schools,
    }, context_instance=RequestContext(request))

def _user_organized_schools(user):
    """
    Schools the user has added an organizer for.
    """
    organizers = Organizer.objects.filter(
        added_by=user,
        content_type=ContentType.objects.get_for_model(School)
    )
    return [o.content_object for o in organizers]

def _user_watched_schools(user):
    """
    Schools the user is watching.
    """
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    return list(user_profile.schools_following.all())
