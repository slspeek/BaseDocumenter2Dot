import unohelper
from com.sun.star.awt import XActionListener
from bd_to_dot import verify_queries
from msgbox import MsgBox


def verifyDialog(ctx=None):
    dlg = createVerifyDialog(ctx)
    dlg.execute()
    dlg.dispose()


def createVerifyDialog(ctx=None):
    smgr = ctx.getServiceManager()
    dp = smgr.createInstanceWithContext("com.sun.star.awt.DialogProvider", ctx)
    dlg = dp.createDialog(
        "vnd.sun.star.script:bd_to_dot_ui.VerifyQueriesDialog.xdl?"
        "location=application")
    startButton = dlg.getControl("Start")
    startButton.addActionListener(ButtonListener(ctx, dlg))
    return dlg


class ButtonListener(unohelper.Base, XActionListener):
    def __init__(self, ctx, dlg):
        self.ctx = ctx
        self.dlg = dlg

    def disposing(self, ev):
        pass

    def actionPerformed(self, ev):
        errors = verify_queries(ctx2datasource(self.ctx))
        if len(errors) > 0:
            errors = self.dlg.getControl("output")
            #  TODO edit dialog
        else:
            myBox = MsgBox(self.ctx)
            myBox.addButton("Yes")
            myBox.renderFromBoxSize(150)
            myBox.numberOflines = 2
            myBox.show("All queries can run", 0, "Success")


def ctx2datasource(ctx):
    sm = ctx.ServiceManager
    d = sm.createInstance("com.sun.star.frame.Desktop")
    return d.CurrentComponent.CurrentController.DataSource
