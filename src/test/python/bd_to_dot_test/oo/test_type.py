from bd_to_dot.oo.db import Object, TYPE


def test_type_view():
    obj = Object(1, 1, 'Table', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert "View" == TYPE(obj)


def test_type_field():
    obj = Object(1, 1, 'Field', "vwPlant",
                 "vwPlant", 0, 0, [2], [4, 5], {'TableIsView': True})
    assert "Field" == TYPE(obj)
