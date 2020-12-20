from bd_to_dot.dot.repository import build_graphs
from bd_to_dot_test.dot.test_objects import objects  # NOQA: F401
from bd_to_dot_test.dot.test_databases import databases  # NOQA: F401
from bd_to_dot.oo.db import Database
from bd_to_dot_test.dot.resource import TEST_OUTPUT
import unittest


def test_build_graphs(objects, databases):  # NOQA: F811
    gs = build_graphs(databases, objects)
    assert len(gs) == 2


class OneDatabaseOnly(unittest.TestCase):

    def setUp(self):
        self.dbs = [
            Database(1, "testdb",
                     {"DocumenterOutputDir":
                        TEST_OUTPUT.format("output-dir")})]
        self.objs = []

    def test_run_empty(self):
        build_graphs(self.dbs, self.objs)
