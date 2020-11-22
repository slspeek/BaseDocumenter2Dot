from collections import namedtuple

Object = namedtuple('Object', ["INDEX", "TYPE", "NAME", "SHORTNAME",
                               "PARENTTYPE", "PARENTINDEX", "USES", "USEDBY",
                               "PROPERTIES"])


def TYPE(object):
    if object.TYPE == 'Table':
        if 'TableIsView' in object.PROPERTIES.keys() and\
           object.PROPERTIES['TableIsView']:
            return 'View'
        else:
            return object.TYPE
    else:
        return object.TYPE
