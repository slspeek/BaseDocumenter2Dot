import time
import logging


logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

# time out in seconds
OFFICE_TIME_OUT = 10


def wait_for_connection():
    import uno

    localContext = uno.getComponentContext()

    # create the UnoUrlResolver
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext
    )

    i = 0
    while i < OFFICE_TIME_OUT * 10:
        try:
            # connect to the running office
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;"
                "urp;StarOffice.ComponentContext"
            )
            break
        except Exception:
            i += 1
            logger.debug("waiting on uno connection for %.0d seconds", i/10)
            time.sleep(0.1)
    else:
        raise Exception("Gave up waiting for libreoffice after {0} seconds"
                        .format(OFFICE_TIME_OUT))
    return ctx.ServiceManager


def smgr():
    return wait_for_connection()


def desktop():
    return smgr().createInstance("com.sun.star.frame.Desktop")


def datasource():
    d = desktop()
    return d.CurrentComponent.CurrentController.DataSource
