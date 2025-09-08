from .models import VisitorLog
from django.utils.deprecation import MiddlewareMixin

class VisitorLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith("/admin/"):
            return

        ip = self.get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        if ip:
            VisitorLog.objects.create(ip_address=ip, user_agent=user_agent)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
