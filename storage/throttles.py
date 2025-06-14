from rest_framework.throttling import SimpleRateThrottle

class PublicLinkThrottle(SimpleRateThrottle):
    scope = "public_link"
    
    def get_cache_key(self, request, view):
        return self.get_ident(request)
    