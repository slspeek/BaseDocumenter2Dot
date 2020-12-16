from bd_to_dot.oo.db import loadObjects
from bd_to_dot.dot.renderer import build_graph


def graph(connection):
    dictObjs = loadObjects(connection)
    g = build_graph(dictObjs)
    return g


def verify_queries(datasource):
    con = datasource.getConnection("", "")
    stmt = con.createStatement()
    errors = []
    for qd in datasource.QueryDefinitions:
        try:
            stmt.executeQuery(qd.Command)
        except Exception as e:
            errors.append((qd.Name, str(e)))
    return errors
