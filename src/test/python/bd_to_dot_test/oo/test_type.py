""" Test the refining of the database object types """
from bd_to_dot.oo.db import Object, object_type


def test_type_view():
    """ Test a refining to View """
    obj = Object(1, 1, 'Table', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert object_type(obj) == "View"


def test_type_field():
    """ Test a non-refining """
    obj = Object(1, 1, 'Field', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert object_type(obj) == "Field"
