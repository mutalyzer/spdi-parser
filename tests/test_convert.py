"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from mutalyzer_spdi_parser.convert import to_model

TESTS_SET = [
    (
        "NG_012337.3:10:C:T",
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 10},
            "deleted": [{"sequence": "C", "source": "description"}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 11},
            "deleted": [{"sequence": "C", "source": "description"}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
    ),
    (
        "NG_012337.3:10:1:T",
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 10},
            "deleted": [{"length": {"type": "point", "value": 1}}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 11},
            "deleted": [{"length": {"type": "point", "value": 1}}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
    ),
    (
        "NG_012337.3:10::T",
    ),
    (
        "NG_012337.3:10:CT:T",
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 10},
            "deleted": [{"sequence": "CT", "source": "description"}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
        {
            "reference": {"id": "NG_012337.3"},
            "location": {
                "type": "range",
                "start": {"type": "point", "position": 11},
                "end": {"type": "point", "position": 12},
            },
            "deleted": [{"sequence": "CT", "source": "description"}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
    ),
    (
        "NG_012337.3:10:2:T",
        {
            "reference": {"id": "NG_012337.3"},
            "location": {"type": "point", "position": 10},
            "deleted": [{"length": {"type": "point", "value": 2}}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
        {
            "reference": {"id": "NG_012337.3"},
            "location": {
                "type": "range",
                "start": {"type": "point", "position": 11},
                "end": {"type": "point", "position": 12},
            },
            "deleted": [{"length": {"type": "point", "value": 2}}],
            "inserted": [{"sequence": "T", "source": "description"}],
            "type": "deletion_insertion",
        },
    ),
]


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[1]) for t in TESTS_SET],
)
def test_convert_raw(description, model):
    assert to_model(description) == model


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[2]) for t in TESTS_SET],
)
def test_convert_hgvs(description, model):
    print(to_model(description, raw=False))
    assert to_model(description, raw=False) == model
