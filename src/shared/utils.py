from typing import Any
from collections import OrderedDict


def refine_serialized_model(ordered_dict: OrderedDict[str, Any]) -> OrderedDict[str, Any]:
    return OrderedDict([(key, ordered_dict[key]) for key in ordered_dict if ordered_dict[key] is not None and ordered_dict[key] != []])
