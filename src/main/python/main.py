from bd_to_dot import graph, verify_queries


def view_graph():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return
    conn = db.getConnection("", "")

    g = graph(conn)
    g.view()


def run_verify_queries():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return

    errors = verify_queries(db)
    if len(errors) > 0:
        raise Exception(str(errors))


g_exportedScripts = (view_graph, run_verify_queries)
