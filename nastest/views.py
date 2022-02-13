from rest_framework.exceptions import ValidationError, NotAcceptable
from rest_framework.viewsets import ViewSet
from .permissions import CheckUserVisit
from rest_framework.decorators import permission_classes
from django.conf import settings
from .json_models import (CarSlot, )
from rest_framework.response import Response
from .utils import error_message, success_message
from .serializers import CarSlotSerializer

class GetInfoView(ViewSet):
    permission_classes = (CheckUserVisit, )

    def list(self, request, *args, **kwargs):
        carslot = CarSlot()
        slot_number = request.GET.get("slot_number")
        if slot_number:
            slot_number = int(slot_number)
        instance = carslot.get(slot_number=slot_number, car_number=request.GET.get("car_number"))
        if len(instance) == 0:
            raise ValidationError(error_message("E_02"))
        return Response(instance)
    
class UnparkView(ViewSet):
    permission_classes = (CheckUserVisit, )
    lookup_field = ('slot_number')

    def destroy(self, request, *args, **kwargs):
        carslot = CarSlot()
        instance = carslot.get(slot_number=int(kwargs.get("slot_number")))
        if len(instance) == 0:
            raise ValidationError(error_message("E_02"))
        instance = carslot.delete(slot_number=int(kwargs.get("slot_number")))
        return Response({"message":success_message("S_01")})

class ParkView(ViewSet):
    permission_classes = (CheckUserVisit, )

    def create(self, request, *args, **kwargs):
        serializer_var = CarSlotSerializer(data=request.data)
        if serializer_var.is_valid(raise_exception=True):
            serializer_var.save()
        return Response({"message":success_message("S_02")})