from bd_to_dot_test.oo.connect import get_context
from bd_to_dot_test.oo.test_db import libreoffice  # NOQA: F401
from bd_to_dot.util.util import invokeMacro


MACRO = "vnd.sun.star.script:BaseDocumenter.BD_API.BD_DocumentDatabase?"\
        "language=Basic&location=application"
MACRO0 = "vnd.sun.star.script:BaseDocumenter.BD_API.BD_OpenRepository?"\
    "language=Basic&location=application"


def test_run_bd(libreoffice):  # NOQA: F811
    ctx = get_context()
    assert invokeMacro(ctx, MACRO0)
    assert invokeMacro(ctx, MACRO)
