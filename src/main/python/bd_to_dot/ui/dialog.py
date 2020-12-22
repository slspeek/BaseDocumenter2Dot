

def verifyDialog(ctx=None):
    smgr = ctx.getServiceManager()
    dp = smgr.createInstanceWithContext("com.sun.star.awt.DialogProvider", ctx)
    dlg = dp.createDialog(
        "vnd.sun.star.script:Standard.VerifyQueriesDialog.xdl?"
        "location=application")
    dlg.execute()
    dlg.dispose()
