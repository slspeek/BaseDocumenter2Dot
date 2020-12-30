""" Top level functions """
from contextlib import contextmanager

from bd_to_dot.oo.db import load_objects, load_databases
from bd_to_dot.dot.repository import build_graphs


@contextmanager
def open_connection(datasource):
    """ contextmanager for libreoffice database connections """
    conn = datasource.getConnection("", "")
    try:
        yield conn
    finally:
        conn.close()
        conn.dispose()


def verify_queries(datasource):
    """ runs all queries of `datasource` and collect errors """
    with open_connection(datasource) as con:
        stmt = con.createStatement()
        errors = []
        for query_def in datasource.QueryDefinitions:
            try:
                stmt.executeQuery(query_def.Command)
            except Exception as ex:  # pylint: disable=broad-except
                errors.append((query_def.Name, str(ex)))
    return errors


def generate_graphs(connection):
    """ generates graphs for all databases in `connection` repository """
    databases = load_databases(connection)
    objects = load_objects(connection)
    build_graphs(databases, objects)
