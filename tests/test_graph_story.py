import pytest

from storygame.Graph_Story import Graph_Story

test_text_1 = "tests/test_text_1.txt"


@pytest.fixture()
def graph_story_empty():
    return Graph_Story()


def test_parse_mermaid_file_story(graph_story_empty: Graph_Story):
    graph_story_empty.parse_mermaid_file_story(test_text_1)
    res = graph_story_empty.print_graph()
    assert (
        res
        == """A[Christmas] -->|Get money| B[Go shopping]
B[Go shopping] --> C[Let me think]
C[Let me think] -->|One| D[Laptop]
C[Let me think] -->|Two| E[iPhone]
C[Let me think] -->|Three| F[fa:fa-car Car]
D[Laptop] --> G
E[iPhone] --> G
F[fa:fa-car Car] --> G
"""
    )
