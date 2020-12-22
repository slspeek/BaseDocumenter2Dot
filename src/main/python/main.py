from bd_to_dot import verify_queries, generate_graphs, open_connection
from bd_to_dot.ui.dialog import verifyDialog


def run_generate_graphs():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return
    with open_connection(db) as conn:
        generate_graphs(conn)


def run_verify_queries():
    try:
        db = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return

    errors = verify_queries(db)
    if len(errors) > 0:
        raise Exception(str(errors))


def run_verify_dialog():
    try:
        ctx = XSCRIPTCONTEXT.getComponentContext()  # NOQA
        verifyDialog(ctx=ctx)
    except AttributeError:
        return


g_exportedScripts = (run_generate_graphs,
                     run_verify_queries, run_verify_dialog)
