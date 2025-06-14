import logging
from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now

access_logger = logging.getLogger("access")
error_logger = logging.getLogger("error")

class AccessLogMiddleware(MiddlewareMixin):
    def process_response(self,request,response):
        if response.status_code in [400,401,403,404,405]:
            user = request.user if request.user.is_authenticated else "Anonymous"
            ip = self._get_client_ip(request)
            log_entry = (
                f"[ACCESS LOG] {now()} | Path: {request.path} | "
                f"Method: {request.method} | IP: {ip} | "
                f"Status: {response.status_code} | User: {user}"
            )
            access_logger.warning(log_entry)
        return response
        
    def process_exception(self, request, exception):
        user = request.user if request.user.is_authenticated else "Anonymous"
        ip = self._get_client_ip(request)
        log_entry = (
            f"[SERVER ERROR] {now()} | Path: {request.path} | "
            f"Method: {request.method} | IP: {ip} |"
            f"User: {user} | Exception: {str(exception)}"
        )
        error_logger.error(log_entry)
        return None
        
    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
    