""" provides a dialog with actionlistener """
import unohelper
from msgbox import MsgBox
from com.sun.star.awt import XActionListener  # pylint: disable=import-error

from bd_to_dot import verify_queries


def verify_dialog(ctx=None):
    """ runs the Verify Queries Dialog """
    dlg = create_verify_dialog(ctx)
    dlg.execute()
    dlg.dispose()


def create_verify_dialog(ctx=None):
    """ create the verify dialog """
    smgr = ctx.getServiceManager()
    dprovider = smgr.createInstanceWithContext(
        "com.sun.star.awt.DialogProvider", ctx)
    dlg = dprovider.createDialog(
        "vnd.sun.star.script:bd_to_dot_ui.VerifyQueriesDialog.xdl?"
        "location=application")
    start_button = dlg.getControl("Start")
    start_button.addActionListener(ButtonListener(ctx, dlg))
    return dlg


class ButtonListener(unohelper.Base, XActionListener):
    """ actionlistener for the start button """

    def __init__(self, ctx, dlg):
        super().__init__()
        self.ctx = ctx
        self.dlg = dlg

    def disposing(self, _):
        """ do nothing on disposing dialog """

    # pylint: disable=invalid-name
    def actionPerformed(self, _):  # NOQA
        """ start the running of the queries and report results """
        errors = verify_queries(ctx2datasource(self.ctx))
        if len(errors) == 0:
            msg_box = MsgBox(self.ctx)
            msg_box.addButton("Yes")
            msg_box.renderFromBoxSize(150)
            msg_box.numberOflines = 2
            msg_box.show("All queries can run", 0, "Success")


def ctx2datasource(ctx):
    """ retrieve datasource from the currently open database file """
    desktop = ctx.ServiceManager.createInstance("com.sun.star.frame.Desktop")
    return desktop.CurrentComponent.CurrentController.DataSource
