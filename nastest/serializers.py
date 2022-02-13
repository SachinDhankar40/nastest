from rest_framework import serializers
from rest_framework.exceptions import ValidationError, NotAcceptable
from .utils import error_message
from .json_models import CarSlot
from django.conf import settings

class CarSlotSerializer(serializers.Serializer):
    car_number = serializers.CharField()

    def validate_car_number(self, car_number):
        car_number = car_number.replace(" ", "")
        if not car_number[0].isalpha():
            raise ValidationError(error_message("E_03"))
        integers = []
        for element in car_number:
            if element.isalpha():
                continue
            elif element.isdigit():
                integers.append(element)
            else:
                raise ValidationError(error_message("E_04"))
        if len(integers) == 0:
            raise ValidationError(error_message("E_05"))
        car_slot = CarSlot()
        car_slot_list = car_slot.list()
        req_list = [i["car_number"] for i in car_slot_list]
        self.slot_list = [i["slot_number"] for i in car_slot_list]
        if car_number in req_list:
            raise ValidationError(error_message("E_06"))
        return car_number

    def create(self, validated_data):
        lot = set(range(0, int(settings.PARKING_LOT_SIZE)))
        available_slots = lot.difference(set(self.slot_list))
        if len(available_slots) == 0:
            raise NotAcceptable(error_message("E_07"))
        validated_data["slot_number"] = list(available_slots)[0]
        car_slot = CarSlot()
        car_slot.create(**validated_data)
        return ""