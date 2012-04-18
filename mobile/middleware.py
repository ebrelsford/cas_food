class MobileMiddleware(object):
    """
    Puts 'IS_MOBILE' in request.META based on user agent.
    """
    MOBILE_UAS = ('iphone', 'android', 'ipad', 'mobile')

    def is_mobile(self, request):
        """                        
        Add is_mobile: True if user agent contains an obvious smartphone, False
        otherwise
        """
        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        return any([mobile_ua in ua for mobile_ua in self.MOBILE_UAS]) 

    def process_request(self, request):
        if self.is_mobile(request):
            request.META['IS_MOBILE'] = True
