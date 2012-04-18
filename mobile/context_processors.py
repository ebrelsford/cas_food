def mobile(request):           
    """                        
    Add is_mobile: True if user agent contains an obvious smartphone, False 
    otherwise
    """
    return { 'is_mobile': request.META.get('IS_MOBILE', False), }
