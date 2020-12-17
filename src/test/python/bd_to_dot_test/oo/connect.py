import time
import logging
import subprocess
import shlex

import uno

logger = logging.getLogger(__name__)
logging.basicConfig()
logger.setLevel(logging.DEBUG)

# time out in seconds
OFFICE_TIME_OUT = 20
SOFFICE_CMD = '/opt/libreoffice6.4/program/soffice '\
              '--accept="socket,host=localhost,port=2002;urp;" '\
              '--norestore --nologo --nodefault  --headless'\
              ' {}'


def startOffice(file):
    args = shlex.split(SOFFICE_CMD.format(file))
    office_proc = subprocess.Popen(args, shell=False)
    logger.debug("LibreOffice started with {} ".format(file))
    return office_proc


def wait_for_connection():
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
            logger.debug(
                "waiting on uno connection for %0.1f seconds", float(i)/10)
            time.sleep(0.1)
    else:
        raise Exception("Gave up waiting for libreoffice after {} seconds"
                        .format(OFFICE_TIME_OUT))
    return ctx.ServiceManager


def smgr():
    return wait_for_connection()


def desktop():
    return smgr().createInstance("com.sun.star.frame.Desktop")


def datasource():
    d = desktop()
    return d.CurrentComponent.CurrentController.DataSource
