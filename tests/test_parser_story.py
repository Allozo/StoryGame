from typing import Optional

import pytest

from storygame.parser_mermaid import ParserMermaid


@pytest.mark.parametrize(
    "node, answer",
    [
        ("name1[text1]", {"node_name": "name1", "node_text": "text1"}),
        ("name2", {"node_name": "name2", "node_text": ""}),
        (
            'name_3[{"author": "Alex", "music": None, "text": "Hello, world!"}]',  # noqa: E501
            {
                "node_name": "name_3",
                "node_text": '{"author": "Alex", "music": None, "text": "Hello, world!"}',  # noqa: E501, C0301; pylint: disable=global-statement
            },
        ),
        ("name4[]", {"node_name": "name4", "node_text": ""}),
        ("", {"node_name": "", "node_text": ""}),
    ],
)
def test_parse_node(node: str, answer: dict[str, str]):
    assert ParserMermaid.parse_node(node) == {
        "node_name": answer["node_name"],
        "node_text": answer["node_text"],
    }


@pytest.mark.parametrize(
    "arrow, answer",
    [
        ("-->", {"text_arrow": ""}),
        ("-->||", {"text_arrow": ""}),
        (
            "-->|Very long and important text|",
            {"text_arrow": "Very long and important text"},
        ),
    ],
)
def test_parse_arrow(arrow: str, answer: dict[str, str]):
    assert ParserMermaid.parse_arrow(arrow) == {
        "text_arrow": answer["text_arrow"]
    }


@pytest.mark.parametrize(
    "line, answer",
    [
        ("A -->|text| B[text]", ("A", " -->|text| ", "B[text]")),
        ("A -->|text| B", ("A", " -->|text| ", "B")),
        ("A --> B[text]", ("A", " --> ", "B[text]")),
        ("A --> B", ("A", " --> ", "B")),
        ("A[text] -->|text| B[text]", ("A[text]", " -->|text| ", "B[text]")),
        ("A[text] -->|text| B", ("A[text]", " -->|text| ", "B")),
        ("A[text] --> B[text]", ("A[text]", " --> ", "B[text]")),
        ("A --> B", ("A", " --> ", "B")),
        ("ASD", None),
    ],
)
def test_parse_line(line: str, answer: Optional[tuple[str, str, str]]):
    res = ParserMermaid.parse_line(line)
    if res is None:
        assert res is None
    assert res == answer
