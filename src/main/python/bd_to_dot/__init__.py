from bd_to_dot.oo.db import loadObjects, loadDatabases
from bd_to_dot.dot.repository import build_graphs


def verify_queries(datasource):
    con = datasource.getConnection("", "")
    stmt = con.createStatement()
    errors = []
    for qd in datasource.QueryDefinitions:
        try:
            stmt.executeQuery(qd.Command)
        except Exception as e:
            errors.append((qd.Name, str(e)))
    con.close()
    con.dispose()
    return errors


def generate_graphs(connection):
    databases = loadDatabases(connection)
    objects = loadObjects(connection)
    graphs = build_graphs(databases, objects)
    for _, g in graphs:
        g.view()
