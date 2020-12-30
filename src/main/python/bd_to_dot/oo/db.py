""" Facilitates the reading of a BaseDocumenter repository """
from collections import namedtuple
import json

Object = namedtuple('Object', ["DATABASEID", "INDEX", "TYPE", "NAME",
                               "SHORTNAME",
                               "PARENTTYPE", "PARENTINDEX", "USES", "USEDBY",
                               "PROPERTIES"])
Database = namedtuple('Database', ["ID", "NAME", "SETTINGS"])


def object_type(obj):
    """ Refines into two extra database object types """
    if obj.TYPE == 'Table':
        if 'TableIsView' in obj.PROPERTIES.keys() and\
           obj.PROPERTIES['TableIsView']:
            return 'View'
        return obj.TYPE
    if obj.TYPE == 'Control':
        if 'ControlType' in obj.PROPERTIES.keys() and\
           obj.PROPERTIES['ControlType'] == "SUBFORMCONTROL":
            return 'SubForm'
        return obj.TYPE
    return obj.TYPE


def _int_list(value):
    if value == '':
        return []
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


def load_objects(connection):
    """ Reads OBJECTS table into [Objects]"""
    stmt = connection.createStatement()
    result_set = stmt.executeQuery(OBJECTS_QUERY)
    objs = []
    while result_set.next():
        properties = json.loads(result_set.getString(12))
        obj = Object(result_set.getInt(1),
                     result_set.getInt(2),
                     result_set.getString(3),
                     result_set.getString(4),
                     result_set.getString(5),
                     result_set.getString(6),
                     result_set.getInt(7),
                     _int_list(result_set.getString(9)),
                     _int_list(result_set.getString(10)),
                     properties)
        obj = obj._replace(TYPE=object_type(obj))
        objs.append(obj)

    return objs


def load_databases(connection):
    """ Reads the DATABASE table into memory """
    stmt = connection.createStatement()
    result_set = stmt.executeQuery(DATABASES_QUERY)
    dbs = []
    while result_set.next():
        settings = json.loads(result_set.getString(10))
        dbs.append(Database(result_set.getInt(1),
                            result_set.getString(2),
                            settings))

    return dbs
