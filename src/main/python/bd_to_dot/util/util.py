

def invokeMacro(ctx, macro_uri):
    sm = ctx.ServiceManager
    mspf = sm.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory",
        ctx)
    scriptPro = mspf.createScriptProvider("")
    xScript = scriptPro.getScript(macro_uri)
    return xScript.invoke((), (), ())
