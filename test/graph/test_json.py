# !#/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch
from os import getenv

from src.graph.json import *


class NodeTestCase(TestCase):
    NAME = "name"
    TARGET = "target"

    def test_node(self):
        node = Node(self.NAME)
        pos = (0, 0)
        self.assertDictEqual(node.node(pos, False), {
            "data": {
                "id": '1',
                "label": self.NAME,
                'expanded': False
            }, 'position': {'x': 0, 'y': 0}
        })
        node.add_value("value")
        self.assertDictEqual(node.node(pos, True), {
            "data": {
                "id": '1',
                "label": "value",
                'expanded': True
            }, 'position': {'x': 0, 'y': 0}
        })

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_edge(self, _):
        node = Node(self.NAME)
        target = Node(self.TARGET)
        self.assertDictEqual(node.edge(target), {
            "data": {
                "label": f"{self.NAME} - {self.TARGET}",
                "source": '1',
                "target": '1'
            }
        })

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_get_empty(self, _):
        node = Node(self.NAME)
        graph = node.get()
        self.assertListEqual(graph, [{
            'data': {"id": "1", "label": self.NAME, "expanded": False},
            'position': {'x': 0, 'y': 0}
        }])

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_get_nested(self, _):
        node = Node(self.NAME)
        target = Node(self.TARGET)
        leaf = "leaf"

        node.add_child(target)
        target.add_child(Node(leaf))
        self.assertListEqual(node.get(), [
            {'data': {'id': '1', 'label': self.NAME, 'expanded': True}, 'position': {'y': 0.0, 'x': 0.0}},
            {"data": {"id": '1', "label": self.TARGET, 'expanded': True}, 'position': {'y': 0.0, 'x': Node.OFFSET[1]}},
            {"data": {"id": '1', "label": leaf, 'expanded': False}, 'position': {'y': 0.0, 'x': Node.OFFSET[1]*2}},
            {"data": {"label": f'{self.TARGET} - {leaf}', "source": '1', "target": '1'}},
            {"data": {"label": f'{self.NAME} - {self.TARGET}', "source": '1', "target": '1'}}
        ])

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_get_several(self, _):
        node = Node(self.NAME)
        target = Node(self.TARGET)
        target2 = Node(f'{self.TARGET}2')

        node.add_child(target)
        node.add_child(target2)
        self.assertListEqual(node.get(), [
            {'data': {'id': '1', 'label': self.NAME, 'expanded': True}, 'position': {'y': Node.OFFSET[0]/2, 'x': 0.0}},
            {"data": {"id": '1', "label": self.TARGET, 'expanded': False}, 'position': {'y': 0.0, 'x': Node.OFFSET[1]}},
            {"data": {"id": '1', "label": f'{self.TARGET}2', 'expanded': False},
             'position': {'y': Node.OFFSET[0], 'x': Node.OFFSET[1]}},
            {'data': {'label': f'{self.NAME} - {self.TARGET}', 'source': '1', 'target': '1'}},
            {"data": {"label": f'{self.NAME} - {self.TARGET}2', "source": '1', "target": '1'}}
        ])


class JsonGraphTestCase(TestCase):
    PROJECT_PATH = getenv('PYTHON_PATH', '.')

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_empty(self, _):
        graph = JsonGraph({})
        self.assertListEqual(graph.tree.children, [])

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_from_file(self, _):
        path = Path(f"{self.PROJECT_PATH}/rsc/empty.json")
        graph = JsonGraph.from_file(path)
        self.assertListEqual(graph.tree.children, [])

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_simple(self, _):
        graph = JsonGraph({"name": "value"})
        self.assertEqual(graph.get().__len__(), 3)
        node = graph.tree.children[0]
        self.assertEqual(node.name, "name")
        self.assertTrue(node.leaf)
        self.assertEqual(node.value, "value")

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_sample(self, _):
        path = Path(f"{self.PROJECT_PATH}/rsc/sample.json")
        graph = JsonGraph.from_file(path)
        with open(Path(f"{self.PROJECT_PATH}/rsc/result.json"), 'r') as f:
            data = loads(f.read())
        self.assertListEqual(graph.get(), data)

    @patch('src.graph.json.Node.generate_id', return_value=1)
    def test_depth(self, _):
        path = Path(f"{self.PROJECT_PATH}/rsc/sample.json")
        graph = JsonGraph.from_file(path)
        with open(Path(f"{self.PROJECT_PATH}/rsc/depth_result.json"), 'r') as f:
            data = loads(f.read())
        self.maxDiff = None
        self.assertListEqual(graph.get(2), data)
