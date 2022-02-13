import os
import json
from rest_framework.exceptions import ValidationError
from django.conf import settings
from .utils import error_message

class JsonModel():
    '''
        Base class to inherit basic cruds for json models like models.Model.
    '''
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.instance = {}
        self.req_list = json.loads(open(os.path.join(settings.BASE_DIR,f'nastest/json_libs/{self.sheet_name}')).read())

    def list(self, **kwargs):
        return self.req_list

    def argument_validator(self, **kwargs):
        kwargs = {key:value for key, value in kwargs.items() if value != None} # removes the None value from kwargs.
        req_fields = kwargs.keys()
        not_present = set(req_fields).difference(set(self.fields.keys()))
        if len(not_present) != 0:
            raise ValidationError("Got unexpected argument {}.".format(list(not_present)[0]))
        return kwargs

    def get(self, **kwargs):
        kwargs = self.argument_validator(**kwargs)
        req_values = set(kwargs.values())
        if len(req_values) != 0:
            for values in self.req_list:
                if req_values.issubset(set(values.values())):
                    self.instance = values
                    return values
        return {}

    def create(self, **kwargs):
        kwargs = self.argument_validator(**kwargs)
        all_present = all([True if value.__class__.__name__==self.fields[key] else False for key, value in kwargs.items()]) # validates the values type
        if all_present:
            self.req_list.append(kwargs)
            self.save(self.req_list)
        else:
            raise ValidationError(error_message("E_08"))

    def update(self, **kwargs):
        kwargs = self.argument_validator(**kwargs)
        all_present = all([True if value.__class__.__name__==self.fields[key] else False for key, value in kwargs.items()])
        if all_present:
            self.delete(**self.instance)
            for key, value in kwargs.items():
                self.instance[key] = value
            self.req_list.append(self.instance)
            self.save(self.req_list)

    def save(self, data, **kwargs):
        with open(os.path.join(settings.BASE_DIR,f'nastest/json_libs/{self.sheet_name}'), "w") as outfile:
            outfile.write(json.dumps(data))

    def delete(self, **kwargs):
        kwargs = self.argument_validator(**kwargs)
        req_values = set(kwargs.values())
        if len(req_values) != 0:
            for values in self.req_list:
                if req_values.issubset(set(values.values())):
                    self.req_list.remove(values)
                    break
        self.save(self.req_list)
        return {}

class UserVisit(JsonModel):
    fields = {
        "ip_address": "str",
        "count": "int",
        "time": "str"
    }

    def __init__(self):
        super().__init__(sheet_name="{}.json".format((self.__class__.__name__).lower()))

class CarSlot(JsonModel):
    fields = {
        "slot_number": "int",
        "car_number": "str"
    }

    def __init__(self):
        super().__init__(sheet_name="{}.json".format((self.__class__.__name__).lower()))