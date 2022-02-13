from django.utils.deprecation import MiddlewareMixin
from nastest.json_models import UserVisit
from datetime import datetime

class RatelimiterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        uservisit = UserVisit()
        instance = uservisit.get(ip_address=ip)
        if len(instance) == 0:
            now = datetime.now()
            uservisit.create(ip_address=ip, count=0, time=str(now).split(".")[0])
        else:
            count = instance["count"]
            count += 1
            uservisit.update(count = count)
        return None