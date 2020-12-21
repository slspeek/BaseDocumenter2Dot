from collections import namedtuple
import json

Object = namedtuple('Object', ["DATABASEID", "INDEX", "TYPE", "NAME",
                               "SHORTNAME",
                               "PARENTTYPE", "PARENTINDEX", "USES", "USEDBY",
                               "PROPERTIES"])
Database = namedtuple('Database', ["ID", "NAME", "SETTINGS"])


def TYPE(object):
    if object.TYPE == 'Table':
        if 'TableIsView' in object.PROPERTIES.keys() and\
           object.PROPERTIES['TableIsView']:
            return 'View'
        else:
            return object.TYPE
    else:
        if object.TYPE == 'Control':
            if 'ControlType' in object.PROPERTIES.keys() and\
               object.PROPERTIES['ControlType'] == "SUBFORMCONTROL":
                return 'SubForm'
            else:
                return object.TYPE
    return object.TYPE


def _int_list(value):
    if value == '':
        return []
    else:
        return list(map(int, value.split("|")))


DATABASES_QUERY = """SELECT "ID",
        "NAME",
        "LOCATION",
        "VERSION",
        "SCANSTATUS",
        "SCANLOG",
        "DOCSTATUS",
        "DOCLOG",
        "TOC",
        "SETTINGS",
        "PROPERTIES"
        FROM "DATABASES" WHERE "ID" <> 0"""

OBJECTS_QUERY = """SELECT "DATABASEID",
       "INDEX",
       CASE "TYPE"
           WHEN 0 THEN 'Database'
           WHEN 1 THEN 'Table'
           WHEN 2 THEN 'Query'
           WHEN 3 THEN 'Form'
           WHEN 4 THEN 'Report'
           WHEN 5 THEN 'Dialog'
           WHEN 6 THEN 'Module'
           WHEN 7 THEN 'Toolbar'
           WHEN 8 THEN 'Field'
           WHEN 9 THEN 'SubForm'
           WHEN 10 THEN 'Grid'
           WHEN 11 THEN 'Control'
           WHEN 12 THEN 'Event'
           WHEN 13 THEN 'Procedure'
           WHEN 14 THEN 'Toolbarcontrol'
           ELSE '???'
       END AS "ITEM TYPE",
       "NAME",
       "SHORTNAME",
       CASE "PARENTTYPE"
           WHEN 0 THEN 'Database'
           WHEN 1 THEN 'Table'
           WHEN 2 THEN 'Query'
           WHEN 3 THEN 'Form'
           WHEN 4 THEN 'Report'
           WHEN 5 THEN 'Dialog'
           WHEN 6 THEN 'Module'
           WHEN 7 THEN 'Toolbar'
           WHEN 8 THEN 'Field'
           WHEN 9 THEN 'SubForm'
           WHEN 10 THEN 'Grid'
           WHEN 11 THEN 'Control'
           WHEN 12 THEN 'Event'
           WHEN 13 THEN 'Procedure'
           WHEN 14 THEN 'Toolbarcontrol'
           ELSE '???'
       END AS "PARENT TYPE",
       "PARENTINDEX",
       "MISSING",
       "USES",
       "USEDBY",
       CHAR_LENGTH ("PROPERTIES") AS "PROPLENGTH",
       "PROPERTIES"
FROM "OBJECTS"
"""


def loadObjects(connection):
    stmt = connection.createStatement()
    rs = stmt.executeQuery(OBJECTS_QUERY)
    objs = []
    while rs.next():
        properties = json.loads(rs.getString(12))
        o = Object(rs.getInt(1),
                   rs.getInt(2),
                   rs.getString(3),
                   rs.getString(4),
                   rs.getString(5),
                   rs.getString(6),
                   rs.getInt(7),
                   _int_list(rs.getString(9)),
                   _int_list(rs.getString(10)),
                   properties)
        o = o._replace(TYPE=TYPE(o))
        objs.append(o)

    return objs


def loadDatabases(connection):
    stmt = connection.createStatement()
    rs = stmt.executeQuery(DATABASES_QUERY)
    dbs = []
    while rs.next():
        settings = json.loads(rs.getString(10))
        d = Database(rs.getInt(1),
                     rs.getString(2),
                     settings)
        dbs.append(d)

    return dbs
