from graphviz import Digraph
from bd_to_dot import Object
from bd_to_dot.dot.renderer import render_object
import unittest


tablePlant = Object(1, 'Table', "Plant", "Plant", 0, 0, [2], [4, 5], "{}")


class TestRendererOnTables(unittest.TestCase):

    def setUp(self):
        g = Digraph("test")
        render_object(tablePlant, g)
        self.line = g.body[0]

    def test_displays_name(self):
        line = self.line
        assert line.find("label=Plant") > 0

    def test_shape_for_table(self):
        line = self.line
        assert line.find("shape=cylinder") > 0


viewPlant = Object(1, 'Query', "Plant", "Plant", 0, 0, "2", "[4,5]", "{}")


class TestRendererOnViews(unittest.TestCase):

    def setUp(self):
        g = Digraph("test")
        render_object(viewPlant, g)
        self.line = g.body[0]

    def test_displays_name(self):
        line = self.line
        assert line.find("label=Plant") > 0

    def test_shape_for_view(self):
        line = self.line
        assert line.find("shape=ellipse") > 0
