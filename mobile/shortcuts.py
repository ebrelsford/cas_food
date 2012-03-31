from django.shortcuts import render_to_response as r2r

from school_food_site.settings import TEMPLATE_MOBILE_DIR, TEMPLATE_SCREEN_DIR

def render_to_response(template, context={}, context_instance=None):
    """
    Wraps django.shortcuts.render_to_response, changing the template dir based 
    on IS_MOBILE in the request context, which should be put there by 
    middleware.
    """
    return r2r(get_template(template, context_instance['request']), context, context_instance=context_instance)

def get_template(template, request):
    template_dir = TEMPLATE_SCREEN_DIR
    if request.META.get('IS_MOBILE', False):
        template_dir = TEMPLATE_MOBILE_DIR
    return "%s/%s" % (template_dir, template)
