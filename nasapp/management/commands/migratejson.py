import os
import json
import inspect
from django.core.management.base import BaseCommand
from django.conf import settings
from nastest import json_models

class Command(BaseCommand):
    help = "creates json file corresponding to json models classes in json_models."

    def handle(self, *args, **options):
        for name, obj in inspect.getmembers(json_models):
            if inspect.isclass(obj):
                parent_class = inspect.getmro(obj)[1]
                if parent_class.__name__ == "JsonModel": # created .json files for all json models inherited from JsonModel
                    file_path = os.path.join(settings.BASE_DIR,f'nastest/json_libs/{name.lower()}.json')
                    if not os.path.exists(file_path):
                        with open(file_path, 'a+') as f:
                            f.write(json.dumps([]))