import re
import yaml
from typing import Any, Dict, List
from spotto_league.models import *  # noqa


class DataCreator:
    __slots__ = ['_yml_data']

    def __init__(self) -> None:
        yml_path = 'tests/config/data.yml'
        with open(yml_path, 'r') as yml:
            self._yml_data = yaml.safe_load(yml)

    def create(self, yml_title: str, overrided_dict: Dict[str, Any]={}) -> Any:
        target = self._yml_data[yml_title]
        instances = self._make_instances(target, overrided_dict)
        if len(instances) == 1:
            return instances[0]
        return instances

    def _to_klass(self, klass_name: str) -> Any:
        return globals()[self._get_klass_name(klass_name)]

    def _get_klass_name(self, origin_name: str) -> str:
        return origin_name.split('_')[0]

    def _make_instances(self, data_dict: Dict[str, Any], overrided_dict: Dict[str, Any]={}) -> Any:
        instances: List[Any] = []
        for klass_name, values in data_dict.items():
            instance = self._make_instance(klass_name, values, overrided_dict)
            instances.append(instance)
            related_classes_data = values.get('related_classes', {})
            related_dict = self._make_related_dict(instance)
            self._make_instances(related_classes_data, related_dict)
        return instances

    def _make_instance(self, klass_name: str, values: Dict[str, Any], overrided_dict: Dict[str, Any]={}) -> Any:
        klass = self._to_klass(klass_name)
        instance = klass()
        properties = values["properties"]
        properties.update(overrided_dict)
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
