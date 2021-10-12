"""
Tests for the lark tree to dictionary converter.
"""

import pytest

from mutalyzer_spdi_parser.convert import to_model

TESTS_SET = [
    (
        "NG_012337.3:10:C:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_sequence": "C",
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "deleted": [{"sequence": "C", "source": "description"}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:1:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 1,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "deleted": [{"length": {"type": "point", "value": 1}}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10::T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:CT:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_sequence": "CT",
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "deleted": [{"sequence": "CT", "source": "description"}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
    (
        "NG_012337.3:10:2:T",
        {
            "seq_id": "NG_012337.3",
            "position": 10,
            "deleted_length": 2,
            "inserted_sequence": "T",
        },
        {
            "type": "description_dna",
            "reference": {"id": "NG_012337.3"},
            "variants": [
                {
                    "location": {
                        "type": "range",
                        "start": {"type": "point", "position": 10},
                        "end": {"type": "point", "position": 11},
                    },
                    "deleted": [{"length": {"type": "point", "value": 2}}],
                    "inserted": [{"sequence": "T", "source": "description"}],
                }
            ],
        },
    ),
]


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[1]) for t in TESTS_SET],
)
def test_convert_spdi(description, model):
    assert to_model(description) == model


@pytest.mark.parametrize(
    "description, model",
    [(t[0], t[2]) for t in TESTS_SET],
)
def test_convert_hgvs(description, model):
    print(to_model(description, raw=False))
    assert to_model(description, raw=False) == model
