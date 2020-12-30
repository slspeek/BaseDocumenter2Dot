""" BaseDocumenter2Dot macros """
from bd_to_dot import verify_queries, generate_graphs, open_connection
from bd_to_dot.ui.dialog import verify_dialog


def run_generate_graphs():
    """ Generate graphs for all databases in the BaseDocumenter repository """
    try:
        # pylint: disable=undefined-variable
        datasource = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return
    with open_connection(datasource) as conn:
        generate_graphs(conn)


def run_verify_queries():
    """ Run all queries dry to check for errors """
    try:
        # pylint: disable=undefined-variable
        datasource = XSCRIPTCONTEXT.getDocument().DataSource  # NOQA
    except AttributeError:
        return

    errors = verify_queries(datasource)
    if len(errors) > 0:
        raise Exception(str(errors))


def run_verify_dialog():
    """ Test the Verify Queries Dialog """
    try:
        # pylint: disable=undefined-variable
        ctx = XSCRIPTCONTEXT.getComponentContext()  # NOQA
        verify_dialog(ctx=ctx)
    except AttributeError:
        return


g_exportedScripts = (run_generate_graphs,
                     run_verify_queries,
                     run_verify_dialog)
