import logging
import subprocess
import shlex
import os

from pytest import fixture

logger = logging.getLogger()
logging.basicConfig()
logger.setLevel(logging.DEBUG)

SOFFICE_CMD = '/opt/libreoffice6.4/program/soffice '\
              '--accept="socket,host=localhost,port=2002;urp;" '\
              '--norestore --nologo --nodefault  --headless'\
              ' src/test/resources/testdb/BaseDocumenter.odb'

@fixture
def libreoffice():
    office_proc = subprocess.Popen(shlex.split(SOFFICE_CMD), shell=False)
    logger.debug("LibreOffice started")
    yield office_proc
    office_proc.terminate()
    # os.system("pkill -9 soffice")
    logger.debug("LibreOffice killed")




def test_connection(libreoffice):
    from bd_to_dot.connect import datasource
    assert datasource().Name.endswith("BaseDocumenter.odb")
