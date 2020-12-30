""" Experimental calling of the calling of BaseDocumenter API """
from bd_to_dot_test.oo.connect import get_context
from bd_to_dot_test.oo.test_db import libreoffice  # pylint: disable=unused-import
from bd_to_dot.util.util import invoke_macro


MACRO = "vnd.sun.star.script:BaseDocumenter.BD_API.BD_DocumentDatabase?"\
        "language=Basic&location=application"
MACRO0 = "vnd.sun.star.script:BaseDocumenter.BD_API.BD_OpenRepository?"\
    "language=Basic&location=application"


# pylint: disable=unused-argument,redefined-outer-name
def test_run_bd(libreoffice):
    """ Do calls in BaseDocumenter extension """
    ctx = get_context()
    assert invoke_macro(ctx, MACRO0)
    assert invoke_macro(ctx, MACRO)
