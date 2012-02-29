from django.shortcuts import get_object_or_404
from django.template import RequestContext

from cas_food.shortcuts import render_to_response
from models import Dish

def menu(request):
    return render_to_response('food/menu.html', {
        'dishes': Dish.objects.all().order_by('name'),
    }, context_instance=RequestContext(request))

def details(request, id=None):
    dish = get_object_or_404(Dish, id=id)
    return render_to_response('food/details.html', {
        'dish': dish,
    }, context_instance=RequestContext(request))

