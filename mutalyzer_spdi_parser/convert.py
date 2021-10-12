"""
Module for converting SPDI descriptions and lark parse trees
to their equivalent dictionary models.
"""

from copy import deepcopy

from lark import Transformer

from .spdi_parser import parse


def to_model(description, raw=True):
    """
    Convert an SPDI description to a dictionary model.
    :arg str description: SPDI description.
    :returns: Description dictionary model.
    :rtype: dict
    """
    return parse_tree_to_model(parse(description), raw)


def parse_tree_to_model(parse_tree, raw=True):
    """
    Convert a parse tree to a dictionary model.
    :arg lark.Tree parse_tree: SPDI description equivalent parse tree.
    :returns: Description dictionary model.
    :rtype: dict
    """
    raw_model = Converter().transform(parse_tree)
    if raw:
        return raw_model
    else:
        return _to_hgvs(raw_model)


class Converter(Transformer):
    def description(self, children):
        return {k: v for d in children for k, v in d.items()}

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


def _to_hgvs(s_m):
    m = {"type": "description_dna", "reference": {"id": s_m["seq_id"]}}
    v = {}
    if s_m.get("deleted_sequence"):
        v["location"] = _range(
            s_m["position"] + 1, s_m["position"] + len(s_m["deleted_sequence"])
        )
        v["deleted"] = [
            {"sequence": s_m["deleted_sequence"], "source": "description"}
        ]
    elif s_m.get("deleted_length"):
        v["location"] = _range(
            s_m["position"] + 1, s_m["position"] + s_m["deleted_length"]
        )
        v["deleted"] = [
            {"length": {"type": "point", "value": s_m["deleted_length"]}}
        ]
    if s_m.get("inserted_sequence"):
        v["location"] = _range(s_m["position"], s_m["position"] + 1)
        v["inserted"] = [
            {"sequence": s_m["inserted_sequence"], "source": "description"}
        ]
    m["variants"] = [v]
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
