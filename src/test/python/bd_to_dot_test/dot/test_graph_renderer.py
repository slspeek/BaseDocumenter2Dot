""" Tests some aspects of GraphRenderer """
import unittest
from bd_to_dot.oo.db import Object
from bd_to_dot.dot.renderer import GraphRenderer

DATABASE_OBJ = Object(1, 0, "Database", "testdb", "testdb",
                      "Database", 0, [], [], {})
TABLE_OBJ = Object(1, 1, 'Table', "Plant", "Plant", "Database", 0, [], [2], {})
VIEW_OBJ = Object(1, 2, 'View', "vwPlant", "vwPlant",
                  "Database", 0, [1], [], {'TableIsView': True})
FIELD_OBJ = Object(1, 3, 'Field', "INDEX", "INDEX",
                   "View", 2, [1], [], {})


class GraphRendererRelatedObjsEmpty(unittest.TestCase):
    """ See that no objects are related in a empty test set """

    def setUp(self):
        self.objs_dict = {0: DATABASE_OBJ}
        self.renderer = GraphRenderer("testdb", self.objs_dict, ["Database"])

    def test_related_empty(self):
        """ See that there are no related objects """
        # pylint: disable=protected-access
        assert len(self.renderer._related_objs()) == 0

    def test_parent_related_empty(self):
        """ No parent child relations """
        # pylint: disable=protected-access
        assert len(self.renderer._parent_relations()) == 0


class GraphRendererRelatedObjsOne(unittest.TestCase):
    """ One relation entry """

    def setUp(self):
        self.objs_dict = {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}
        self.renderer = GraphRenderer("testdb", self.objs_dict, ["Database"])
        # pylint: disable=protected-access
        self.related = self.renderer._related_objs()

    def test_filtered_objs(self):
        """ all object pass the filter """
        assert len(self.renderer.objs) == 2

    def test_related_size_is_one(self):
        """ exactely one related pair """
        assert len(self.related) == 1

    def test_related(self):
        """ check the related pair """
        assert (VIEW_OBJ, TABLE_OBJ) in self.related


class TestRendererOnTables(unittest.TestCase):
    """ See some code produced by tables """

    def setUp(self):
        self.renderer = GraphRenderer(
            "testdb",
            {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}, [])
        # pylint: disable=protected-access
        self.renderer._render_object(TABLE_OBJ)
        self.line = self.renderer.graph.body[len(self.renderer.graph.body)-1]

    def test_displays_name(self):
        """ Is table name visible """
        assert self.line.find("label=Plant") > 0

    def test_shape_for_table(self):
        """ Is the shape good """
        assert self.line.find("shape=cylinder") > 0


class TestRendererOnViews(unittest.TestCase):
    """ See results produced for a View """

    def setUp(self):
        self.renderer = GraphRenderer(
            "testdb",
            {0: DATABASE_OBJ, 1: TABLE_OBJ, 2: VIEW_OBJ}, [])
        # pylint: disable=protected-access
        self.renderer._render_object(VIEW_OBJ)
        self.line = self.renderer.graph.body[len(self.renderer.graph.body)-1]

    def test_displays_name(self):
        """ View name displayed """
        assert self.line.find("label=vwPlant") > 0

    def test_shape_for_view(self):
        """ Shape is for Views """
        assert self.line.find("shape=hexagon") > 0
