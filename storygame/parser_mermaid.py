from pathlib import Path
import re
from typing import Optional


# В тексте нельзя использовать символы "[" и "]"
symbol_in_text = [
    "\w",
    " ",
    "\\",
    "/",
    ",",
    ".",
    "?",
    ";",
    ":",
    "'",
    '"',
    "|",
    "(",
    ")",
    "!",
    "@",
    "#",
    "№",
    "$",
    "%",
    "^",
    "&",
    "*",
    "+",
    "-",
    "=",
    "_",
    "{",
    "}",
]
text_in_arrow_and_node = "|\\".join(symbol_in_text)

name_node_without_text = f"\w+"
name_node_with_text = f"\w+\[[{text_in_arrow_and_node}]+\]"
arrow_with_text = f" *-->\|[{text_in_arrow_and_node}]*\| *"
arrow_without_text = f" *--> *"


class ParserMermaid:
    @staticmethod
    def create_list_pattern() -> list[str]:
        """
        Будем парсить следующие случаи

        1. A[Christmas] -->|Get money| B[Go shopping]
        2. A[Christmas] -->|Get money| B
        3. A[Christmas] --> B[Go shopping]
        4. A[Christmas] --> B
        5. A -->|Get money| B[Go shopping]
        6. A -->|Get money| B
        7. A --> B[Go shopping]
        8. A --> B
        """

        list_pattern = [
            rf"(({i})({j})({k}))"
            for i in (name_node_with_text, name_node_without_text)
            for j in (arrow_with_text, arrow_without_text)
            for k in (name_node_with_text, name_node_without_text)
        ]

        return list_pattern

    @staticmethod
    def preprocessing_line(line: str) -> str:
        if line[-1] == "\n":
            line = line[:-1]
        return line

    @staticmethod
    def is_correct_line(line: str) -> bool:
        if "graph TD" in line:
            return False

        if line == "\n":
            return False

        return True

    @staticmethod
    def parse_node(node: str) -> dict[str, str]:
        match_node_with_text = re.search(name_node_with_text, node)
        match_node_without_text = re.search(name_node_without_text, node).group(0)

        # Получаем имя (его мы получили из регулярки без скобок)
        node_name = match_node_without_text

        # Если вершина с текстом в [], получим текст в скобках
        re_node_with_text = f"\w+\[([{text_in_arrow_and_node}]+)\]"
        text_in_node = (
            re.search(re_node_with_text, node).group(1)
            if match_node_with_text is not None
            else None
        )

        return {"node_name": node_name, "node_text": text_in_node}

    @staticmethod
    def parse_arrow(arrow: str) -> dict[str, str]:
        arrow_with_text = f" *-->\|([{text_in_arrow_and_node}]*)\| *"
        text_arrow = re.search(arrow_with_text, arrow)
        if text_arrow is not None:
            text_arrow = text_arrow.group(1)

        return {"text_arrow": text_arrow}

    @staticmethod
    def parse_line(line: str) -> Optional[tuple]:
        list_pattern = ParserMermaid.create_list_pattern()

        for pattern in list_pattern:
            match = re.search(pattern, line)
            if match is not None:
                break
        else:
            # Если не нашли паттерны в строке
            return

        node_left = match.group(2)
        arrow = match.group(3)
        node_right = match.group(4)

        return node_left, arrow, node_right
