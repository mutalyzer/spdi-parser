"""
Module for converting SPDI descriptions and lark parse trees
to their equivalent dictionary models.
"""

from lark import Token, Transformer
from copy import deepcopy
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
        if description.get("deleted") or description.get("inserted"):
            description["type"] = "deletion_insertion"
        else:
            description["type"] = "equal"
        return description

    def deleted(self, children):
        return {"deleted": children}

    def inserted(self, children):
        return {"inserted": children}

    def point(self, children):
        return {"location": {"type": "point", "position": children[0]}}

    def length(self, children):
        return {"length": {"type": "point", "value": children[0]}}

    def NUMBER(self, name):
        return int(name)

    def SEQUENCE(self, name):
        return {"sequence": name.value, "source": "description"}

    def ID(self, name):
        return {"reference": {"id": name.value}}


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
            r_m["deleted"][0].get("length")
            and r_m["deleted"][0]["length"]["value"] > 1
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
