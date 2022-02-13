from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .utils import error_message
from .json_models import UserVisit
from datetime import datetime

class CheckUserVisit(BasePermission):
    '''
        checks wether user is making more than 10 requests in 10 seconds.
    '''
    def has_permission(self, request, view, **kwargs):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        uservisit = UserVisit()
        instance = uservisit.get(ip_address=ip)
        now = datetime.now()
        difference = (now - datetime.strptime(instance["time"], "%Y-%m-%d %H:%M:%S")).total_seconds()
        if difference > 10:
            uservisit.delete(**instance)
            uservisit.create(ip_address=ip, count=0, time=str(datetime.now()).split(".")[0])
            return True
        else:
            if instance["count"] <= 10:
                return True
        raise PermissionDenied(error_message("E_01"))