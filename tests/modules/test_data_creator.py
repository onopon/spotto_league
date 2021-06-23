import re
import yaml
from typing import Any, Dict, List
from spotto_league.models import *  # noqa


class TestDataCreator:
    def create(self, yml_title: str, yml_path: str='tests/config/data.yml') -> Any:
        with open(yml_path, 'r') as yml:
            data = yaml.safe_load(yml)
            target = data[yml_title]
            instances = self._make_instances(target)
        return instances

    def _to_klass(self, klass_name: str) -> Any:
        return globals()[klass_name]

    def _make_instances(self, data_dict: Dict[str, Any], related_dict: Dict[str, Any]={}) -> Any:
        instances: List[Any] = []
        for klass_name, values in data_dict.items():
            instance = self._make_instance(klass_name, values, related_dict)
            instances.append(instance)
            related_classes_data = values.get('related_classes', {})
            related_dict = self._make_related_dict(instance)
            instances.extend(self._make_instances(related_classes_data, related_dict))
        return instances

    def _make_instance(self, klass_name, values: Dict[str, Any], related_dict: Dict[str, Any]={}) -> Any:
        klass = self._to_klass(klass_name)
        instance = klass()
        properties = values["properties"]
        properties.update(related_dict)
        for property_name, val in properties.items():
            setattr(instance, property_name, val)
        instance.save()
        return instance

    def _make_related_dict(self, instance: Any) -> Dict[str, int]:
        klass_name = instance.__class__.__name__
        return {self._make_id(klass_name): instance.id}

    def _make_id(self, klass_name: str) -> str:
        return "{}_id".format(self._camel_to_snake(klass_name))

    def _camel_to_snake(self, s: str) -> str:
        return re.sub("((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", s).lower()
