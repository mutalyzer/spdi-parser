"""
Module for converting SPDI descriptions and lark parse trees
to their equivalent dictionary models.
"""

from copy import deepcopy

from lark import Transformer

from .spdi_parser import parse


def to_model(description, raw=True):
    """
    Convert an SPDI description, or parts of it, e.g., a location,
    a variants list, etc., if an appropriate alternative `start_rule`
    is provided, to a nested dictionary model.
    :arg str description: SPDI description.
    :arg str start_rule: Alternative start rule.
    :returns: Description dictionary model.
    :rtype: dict
    """
    return parse_tree_to_model(parse(description), raw)


def parse_tree_to_model(parse_tree, raw=True):
    """
    Convert a parse tree to a nested dictionary model.
    :arg lark.Tree parse_tree: SPDI description equivalent parse tree.
    :returns: Description dictionary model.
    :rtype: dict
    """
    raw_model = Converter().transform(parse_tree)
    if raw:
        return raw_model
    else:
        return _to_hgvs_location(raw_model)


class Converter(Transformer):
    def description(self, children):
        description = {k: v for d in children for k, v in d.items()}
        return description

    def deleted_sequence(self, children):
        return {"deleted_sequence": children[0]}

    def inserted_sequence(self, children):
        return {"inserted_sequence": children[0]}

    def position(self, children):
        return {"position": children[0]}

    def deleted_length(self, children):
        return {"deleted_length": children[0]}

    def NUMBER(self, name):
        return int(name)

    def SEQUENCE(self, name):
        return name.value

    def ID(self, name):
        return {"seq_id": name.value}


def _to_hgvs_location(r_m):
    m = deepcopy(r_m)
    if r_m.get("deleted"):
        if (
            r_m["deleted"][0].get("length")
            and r_m["deleted"][0]["length"]["value"] == 1
        ) or (
            r_m["deleted"][0].get("sequence")
            and len(r_m["deleted"][0]["sequence"]) == 1
        ):
            m["location"]["position"] = r_m["location"]["position"] + 1
        elif (
            r_m["deleted"][0].get("length") and r_m["deleted"][0]["length"]["value"] > 1
        ):
            m["location"] = _range(
                r_m["location"]["position"] + 1,
                r_m["location"]["position"] + r_m["deleted"][0]["length"]["value"],
            )
        elif r_m["deleted"][0].get("sequence"):
            m["location"] = _range(
                r_m["location"]["position"] + 1,
                r_m["location"]["position"] + len(r_m["deleted"][0]["sequence"]),
            )
    return m


def _range(s, e):
    return {
        "type": "range",
        "start": {
            "type": "point",
            "position": s,
        },
        "end": {
            "type": "point",
            "position": e,
        },
    }
