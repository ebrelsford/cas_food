from django.template import RequestContext

from cas_food.shortcuts import render_to_response

def index(request):
    return render_to_response("getinvolved/index.html", {}, context_instance=RequestContext(request))
