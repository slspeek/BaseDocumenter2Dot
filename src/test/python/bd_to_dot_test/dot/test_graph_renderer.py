from bd_to_dot.oo.db import Object
from bd_to_dot.dot.renderer import GraphRenderer
import unittest

DATABASE_OBJ = Object(1, 0, "Database", "testdb", "testdb",
                      "Database", 0, [], [], {})
TABLE_OBJ = Object(1, 1, 'Table', "Plant", "Plant", "Database", 0, [], [2], {})
VIEW_OBJ = Object(1, 2, 'View', "vwPlant", "vwPlant",
                  "Database", 0, [1], [], {'TableIsView': True})
FIELD_OBJ = Object(1, 3, 'Field', "INDEX", "INDEX",
                   "View", 2, [1], [], {})


class GraphRendererRelatedObjsEmpty(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: DATABASE_OBJ}
        self.gr = GraphRenderer("testdb", self.dictObjs, ["Database"])

    def test_related_empty(self):
        assert len(self.gr._related_objs()) == 0


class GraphRendererRelatedObjsOne(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}
        self.gr = GraphRenderer("testdb", self.dictObjs, ["Database"])
        self.related = self.gr._related_objs()

    def test_filtered_objs(self):
        assert len(self.gr.objs) == 2

    def test_related_size_is_one(self):
        assert len(self.related) == 1

    def test_related(self):
        assert (VIEW_OBJ, TABLE_OBJ) in self.related


class GraphRendererParentRelationsEmpty(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: DATABASE_OBJ}
        self.gr = GraphRenderer("testdb", self.dictObjs, ["Database"])

    def test_related_empty(self):
        assert len(self.gr._parent_relations()) == 0


class GraphRendererParrentRelationsTwo(unittest.TestCase):

    def setUp(self):
        self.dictObjs = {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}
        self.gr = GraphRenderer("testdb", self.dictObjs, [])
        self.related = self.gr._related_objs()

    def test_filtered_objs(self):
        assert len(self.gr.objs) == 3

    def test_related_size_is_one(self):
        assert len(self.related) == 1

    def test_related(self):
        assert (VIEW_OBJ, TABLE_OBJ) in self.related


class TestRendererOnTables(unittest.TestCase):

    def setUp(self):
        self.gr = GraphRenderer(
            "testdb",
            {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}, [])
        self.gr._render_object(TABLE_OBJ)
        self.line = self.gr.graph.body[len(self.gr.graph.body)-1]

    def test_displays_name(self):
        assert self.line.find("label=Plant") > 0

    def test_shape_for_table(self):
        assert self.line.find("shape=cylinder") > 0


class TestRendererOnViews(unittest.TestCase):

    def setUp(self):
        self.gr = GraphRenderer(
            "testdb",
            {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}, [])
        self.gr._render_object(VIEW_OBJ)
        self.line = self.gr.graph.body[len(self.gr.graph.body)-1]

    def test_displays_name(self):
        assert self.line.find("label=vwPlant") > 0

    def test_shape_for_view(self):
        assert self.line.find("shape=hexagon") > 0
