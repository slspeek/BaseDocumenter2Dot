from bd_to_dot import Object
import json


def _int_list(value):
    if value == '':
        return []
    else:
        return list(map(int, value.split("|")))


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
    objs = {}
    while rs.next():
        properties = json.loads(rs.getString(12))
        o = Object(rs.getInt(2),
                   rs.getString(3),
                   rs.getString(4),
                   rs.getString(5),
                   rs.getString(6),
                   rs.getInt(7),
                   _int_list(rs.getString(9)),
                   _int_list(rs.getString(10)),
                   properties)
        objs[o.INDEX] = o

    connection.close()
    connection.dispose()
    return objs
