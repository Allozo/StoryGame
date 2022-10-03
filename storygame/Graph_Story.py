from __future__ import annotations

from dataclasses import dataclass
from parser_mermaid import ParserMermaid as mparse
from pathlib import Path


@dataclass()
class Choice:
    text: str
    to_node: Node

    def __str__(self) -> str:
        res = ""
        if self.text is None:
            res = f" --> {self.to_node}"
        else:
            res = f" -->|{self.text}| {self.to_node}"
        return res


@dataclass()
class Node:
    name: str
    text: str
    choice_list: list[Choice]

    def __str__(self) -> str:
        res = ""
        if self.text is None:
            res = f"{self.name}"
        else:
            res = f"{self.name}[{self.text}]"
        return res


class Graph_Story:
    def __init__(self) -> None:
        self.dict_node = dict()

    def _add_node(self, dict_param: dict) -> None:
        # Если вершина уже есть
        if dict_param["node_name"] in self.dict_node:
            return

        node = Node(
            name=dict_param["node_name"],
            text=dict_param["node_text"],
            choice_list=list(),
        )
        self.dict_node[dict_param["node_name"]] = node

    def _add_arrow(
        self, node_left_name: str, dict_param_choice: dict, node_right_name: str
    ) -> None:
        node_right = self.dict_node[node_right_name]

        choice = Choice(text=dict_param_choice["text_arrow"], to_node=node_right)

        self.dict_node[node_left_name].choice_list.append(choice)

    def parse_mermaid_file_story(self, file_name: str):
        with Path(file_name).open() as file:
            for line in file:
                if not mparse.is_correct_line(line):
                    continue

                line = mparse.preprocessing_line(line)

                node_arrow_node = mparse.parse_line(line)

                if node_arrow_node is None:
                    continue

                str_node_left, str_arrow, str_node_right = node_arrow_node

                dict_left_node = mparse.parse_node(str_node_left)
                dict_arrow = mparse.parse_arrow(str_arrow)
                dict_right_node = mparse.parse_node(str_node_right)

                self._add_node(dict_left_node)
                self._add_node(dict_right_node)
                self._add_arrow(
                    dict_left_node["node_name"],
                    dict_arrow,
                    dict_right_node["node_name"],
                )

    def print_graph(self):
        res = ""
        for node in self.dict_node.values():
            for choice in node.choice_list:
                res += f"{node}{choice}\n"
        return res


if __name__ == "__main__":
    g = Graph_Story()
    g.parse_mermaid_file_story("text.txt")
    print(g.print_graph())
