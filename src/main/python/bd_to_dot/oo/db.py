from bd_to_dot import Object


def loadObjects(connection):
    stmt = connection.createStatement()
    rs = stmt.executeQuery('SELECT "DATABASEID", "INDEX", "TYPE", "NAME", '
                           '"SHORTNAME","PARENTTYPE", "PARENTINDEX", "USES",'
                           '"USEDBY", "PROPERTIES" FROM '
                           '"OBJECTS" WHERE "DATABASEID" = 1')
    objs = {}
    while rs.next():
        o = Object(rs.getInt(2), rs.getInt(3), rs.getString(4),
                   rs.getString(5), rs.getInt(6), rs.getInt(7),
                   rs.getString(8), rs.getString(9),
                   rs.getString(10))
        objs[o.INDEX] = o

    connection.close()
    connection.dispose()
    return objs
