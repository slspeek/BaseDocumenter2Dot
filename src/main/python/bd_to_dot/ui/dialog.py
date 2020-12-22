

def verifyDialog(ctx=None):
    smgr = ctx.getServiceManager()
    dp = smgr.createInstanceWithContext("com.sun.star.awt.DialogProvider", ctx)
    dlg = dp.createDialog(
        "vnd.sun.star.script:bd2dot.oxt|python|VerifyQueriesDialog.xdl?"
        "location=application")
    dlg.execute()
    dlg.dispose()
