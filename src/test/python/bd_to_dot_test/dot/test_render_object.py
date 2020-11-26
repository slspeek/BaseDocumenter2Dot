from graphviz import Digraph
from bd_to_dot.oo.db import Object
from bd_to_dot.dot.renderer import render_object, related_objects,\
    parent_relations
import unittest

database = Object(0, "Database", "testdb", "testdb", "Database", 0, [], [], {})
tablePlant = Object(1, 'Table', "Plant", "Plant", "Database", 0, [], [2], {})
viewPlant = Object(2, 'View', "vwPlant", "vwPlant",
                   "Database", 0, [1], [], {'TableIsView': True})
field = Object(3, 'Field', "INDEX", "INDEX",
               "View", 2, [1], [], {})


class TestRendererOnTables(unittest.TestCase):

    def setUp(self):
        g = Digraph("test")
        render_object(tablePlant, g)
        self.line = g.body[0]

    def test_displays_name(self):
        assert self.line.find("label=Plant") > 0

    def test_shape_for_table(self):
        assert self.line.find("shape=cylinder") > 0


class TestRendererOnViews(unittest.TestCase):

    def setUp(self):
        g = Digraph("test")
        render_object(viewPlant, g)
        self.line = g.body[0]

    def test_displays_name(self):
        assert self.line.find("label=vwPlant") > 0

    def test_shape_for_view(self):
        assert self.line.find("shape=hexagon") > 0


class TestRelatedObjects(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {1: tablePlant, 2: viewPlant}
        self.related = related_objects(self.dictObjs)

    def test_one_realtion(self):
        assert len(self.related) == 1

    def test_related(self):
        assert (viewPlant, tablePlant) in self.related


class TestParentObjects(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database, 1: tablePlant, 2: viewPlant, 3: field}
        self.related = parent_relations(self.dictObjs)

    def test_one_realtion(self):
        assert len(self.related) == 0

    def test_related(self):
        assert (field, viewPlant) not in self.related
