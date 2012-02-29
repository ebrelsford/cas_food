from django.shortcuts import render_to_response as r2r

from settings import TEMPLATE_MOBILE_DIR, TEMPLATE_SCREEN_DIR

def render_to_response(template, context={}, context_instance=None):
    """
    Wraps django.shortcuts.render_to_response, changing the template dir based 
    on IS_MOBILE in the request context, which should be put there by 
    middleware.
    """
    if context_instance['request'].META.get('IS_MOBILE', False):
        template = "%s/%s" % (TEMPLATE_MOBILE_DIR, template)
    else:
        template = "%s/%s" % (TEMPLATE_SCREEN_DIR, template)
    return r2r(template, context, context_instance=context_instance)

