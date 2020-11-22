from collections import namedtuple

Object = namedtuple('Object', ["INDEX", "TYPE", "NAME", "SHORTNAME",
                               "PARENTTYPE", "PARENTINDEX", "USES", "USEDBY",
                               "PROPERTIES"])
