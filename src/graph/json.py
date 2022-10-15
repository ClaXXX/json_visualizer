#!/usr/bin/env python3
from json import loads
from logging import getLogger
from pathlib import Path
from typing import Tuple, Any


class Node:
    OFFSET = (20.0, 400.0)

    cursor = 0

    @classmethod
    def generate_id(cls):
        cls.cursor += 1
        return cls.cursor

    def __init__(self, name: str):
        self.id = Node.generate_id()
        self.name = name
        self.leaf = False
        self.value = None
        self.children = []

    def add_value(self, value):
        self.leaf = True
        self.value = value

    def add_child(self, node):
        self.children.append(node)

    def node(self, pos: Tuple[float, float], expanded: bool):
        return {
            "data": {
                "id": str(self.id),
                "label": str(self.value if self.leaf else self.name),
                "expanded": expanded
            },
            "position": {
                'y': pos[0],
                'x': pos[1]
            }
        }

    def edge(self, target):
        return {
            "data": {
                "source": str(self.id),
                "target": str(target.id),
                "label": f'{self.name} - {target.name}'
            }
        }

    def nested_get(self,
                   nodes: list,
                   edges: list,
                   pos: Tuple[float, float],
                   depth=None):
        if self.leaf or not len(self.children) \
                or (depth is not None and depth == 0):
            nodes.append(self.node(pos, False))
            return pos[0]

        bottom = pos[0]
        _y = pos[1] + self.OFFSET[1]
        if depth:
            depth -= 1
        for child in self.children:
            bottom = child.nested_get(
                nodes, edges, (bottom, _y), depth)
            bottom += self.OFFSET[0]
            edges.append(self.edge(child))
        else:
            bottom -= self.OFFSET[0]
        nodes.insert(0, self.node((pos[0] + ((bottom - pos[0]) / 2), pos[1]), True))
        return bottom

    def get(self, depth=None):
        nodes = []
        edges = []
        self.nested_get(nodes, edges, (0.0, 0.0), depth)
        nodes.extend(edges)
        return nodes


class JsonGraph:
    def __init__(self, data: dict):
        self._logger = getLogger(__name__)
        self.tree = Node('')
        # Items per depth
        self.map(self.tree, data)
        self._logger.info('Tree loaded')

    @classmethod
    def from_file(cls, filepath: Path):
        with open(filepath, 'r') as f:
            return cls(loads(f.read()))

    def map(self, node: Node, value: Any):
        _type = type(value)
        if _type is dict:
            self.dict(node, value)
        elif _type is list:
            self.list(node, value)
        else:
            node.add_value(value)

    def list(self, node: Node, data: list):
        for index, row in enumerate(data):
            child = Node(str(index))
            node.add_child(child)
            self.map(child, row)

    def dict(self, node: Node, data: dict):
        for key in data:
            child = Node(key)
            node.add_child(child)
            self.map(child, data.get(key))

    def get(self, depth=None):
        """
        Return list of elements as cytoscape read it
        """
        return self.tree.get(depth)
