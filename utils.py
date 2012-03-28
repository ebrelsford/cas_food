from django.template.defaultfilters import slugify as _slugify

def slugify(model, text):
    """
    Make a unique slug for an object of the given model with the given text.
    
    Assumes the slug field is called 'slug'.
    """
    slug = _slugify(text)
    same_slug_count = model.objects.filter(slug__iregex=slug + '(-\d+)?').count()
    if same_slug_count:
        slug = "%s-%d" % (slug, same_slug_count)
    return slug
