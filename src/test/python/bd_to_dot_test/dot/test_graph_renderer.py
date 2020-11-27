from bd_to_dot.oo.db import Object
from bd_to_dot.dot.renderer import GraphRenderer
import unittest

database = Object(0, "Database", "testdb", "testdb", "Database", 0, [], [], {})
tablePlant = Object(1, 'Table', "Plant", "Plant", "Database", 0, [], [2], {})
viewPlant = Object(2, 'View', "vwPlant", "vwPlant",
                   "Database", 0, [1], [], {'TableIsView': True})
field = Object(3, 'Field', "INDEX", "INDEX",
               "View", 2, [1], [], {})


class GraphRendererName(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database}
        self.gr = GraphRenderer(self.dictObjs, ["Database"])

    def test_name(self):
        assert "testdb" == self.gr._name()


class GraphRendererNameRaisesNoValue(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {}

    def test_name_raises(self):
        self.assertRaises(ValueError,
                          GraphRenderer,
                          self.dictObjs,
                          ["Database"])


class GraphRendererNameRaisesTooManyValues(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database, 1: database}

    def test_name_raises(self):
        self.assertRaises(ValueError,
                          GraphRenderer,
                          self.dictObjs,
                          ["Database"])


class GraphRendererRelatedObjsEmpty(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database}
        self.gr = GraphRenderer(self.dictObjs, ["Database"])

    def test_related_empty(self):
        assert len(self.gr._related_objs()) == 0


class GraphRendererRelatedObjsOne(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database, 1: tablePlant, 2: viewPlant}
        self.gr = GraphRenderer(self.dictObjs, ["Database"])
        self.related = self.gr._related_objs()

    def test_filtered_objs(self):
        assert len(self.gr.objs) == 2

    def test_related_size_is_one(self):
        assert len(self.related) == 1

    def test_related(self):
        assert (viewPlant, tablePlant) in self.related


class GraphRendererParentRelationsEmpty(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database}
        self.gr = GraphRenderer(self.dictObjs, ["Database"])

    def test_related_empty(self):
        assert len(self.gr._parent_relations()) == 0


class GraphRendererParrentRelationsTwo(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: database, 1: tablePlant, 2: viewPlant}
        self.gr = GraphRenderer(self.dictObjs, [])
        self.related = self.gr._related_objs()

    def test_filtered_objs(self):
        assert len(self.gr.objs) == 3

    def test_related_size_is_one(self):
        assert len(self.related) == 1

    def test_related(self):
        assert (viewPlant, tablePlant) in self.related


class TestRendererOnTables(unittest.TestCase):

    def setUp(self):
        self.gr = GraphRenderer({0: database, 1: tablePlant, 2: viewPlant}, [])
        self.gr._render_object(tablePlant)
        self.line = self.gr.graph.body[0]

    def test_displays_name(self):
        assert self.line.find("label=Plant") > 0

    def test_shape_for_table(self):
        assert self.line.find("shape=cylinder") > 0


class TestRendererOnViews(unittest.TestCase):

    def setUp(self):
        self.gr = GraphRenderer({0: database, 1: tablePlant, 2: viewPlant}, [])
        self.gr._render_object(viewPlant)
        self.line = self.gr.graph.body[0]

    def test_displays_name(self):
        assert self.line.find("label=vwPlant") > 0

    def test_shape_for_view(self):
        assert self.line.find("shape=hexagon") > 0
