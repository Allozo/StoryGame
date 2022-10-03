import re
from typing import Optional

# В тексте нельзя использовать символы "[" и "]"
symbol_in_text = [
    r"\w",
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

name_node_without_text = r"\w+"
name_node_with_text = rf"\w+\[[{text_in_arrow_and_node}]+\]"
arrow_with_text = rf" *-->\|[{text_in_arrow_and_node}]*\| *"
arrow_without_text = r" *--> *"


class ParserMermaid:
    @staticmethod
    def create_list_pattern() -> list[str]:
        """
        Будем парсить следующие случаи

        1. A[text] -->|text| B[text]
        2. A[text] -->|text| B
        3. A[text] --> B[text]
        4. A[text] --> B
        5. A -->|text| B[text]
        6. A -->|text| B
        7. A --> B[text]
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
    def parse_node(node: str) -> dict[str, str]:
        match_node_without_text = re.search(name_node_without_text, node)

        # Получаем имя (его мы получили из регулярки без скобок)
        node_name = ""
        if match_node_without_text is not None:
            node_name = match_node_without_text.group(0)

        # Если вершина с текстом в [], получим текст в скобках
        re_node_with_text = rf"\w+\[([{text_in_arrow_and_node}]+)\]"

        search_text_in_node = re.search(re_node_with_text, node)
        text_in_node = ""
        if search_text_in_node is not None:
            text_in_node = search_text_in_node.group(1)

        return {"node_name": node_name, "node_text": text_in_node}

    @staticmethod
    def parse_arrow(arrow: str) -> dict[str, str]:
        arrow_with_text = rf" *-->\|([{text_in_arrow_and_node}]*)\| *"
        search_text_arrow = re.search(arrow_with_text, arrow)
        text_arrow = ""
        if search_text_arrow is not None:
            text_arrow = search_text_arrow.group(1)

        return {"text_arrow": text_arrow}

    @staticmethod
    def parse_line(line: str) -> Optional[tuple[str, str, str]]:
        list_pattern = ParserMermaid.create_list_pattern()

        for pattern in list_pattern:
            match = re.search(pattern, line)
            if match is not None:
                break
        else:
            # Если не нашли паттерны в строке
            return None

        node_left = match.group(2)
        arrow = match.group(3)
        node_right = match.group(4)

        return node_left, arrow, node_right
