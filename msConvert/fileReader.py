
from os.path import splitext
from queue import Queue
from threading import Thread
import pyopenms

from fileTypes import FileType


def _getFileHandeler(iftype: FileType):
    if iftype == FileType.MZML:
        return pyopenms.MzMLFile()
    elif iftype == FileType.MZXML:
        return pyopenms.MzXMLFile()
    else:
        raise NotImplementedError('{} not implemented!'.format(iftype.value))


def readToPeakMap(ifname, iftype):
    peakMap = pyopenms.MSExperiment()
    fileHandeler = _getFileHandeler(iftype)
    fileHandeler.load(ifname, peakMap)
    return peakMap


def convertFile(ifname : str, iftype: FileType, oftype: FileType, ofname : str = None):
    #read input peak map
    peakMap = readToPeakMap(ifname, iftype)

    #get ofname
    if ofname is None:
        _ofname = '{}.{}'.format(splitext(ifname)[0], oftype.value)
    else: _ofname = ofname

    fileHandeler = _getFileHandeler(oftype)
    fileHandeler.store(_ofname, peakMap)


def _convertFiles_threadHelper(q : Queue, iftype: FileType, oftype: FileType, ofname : str = None):
    while True:
        item = q.get()
        if item is None:
            break
        convertFile(item, iftype, oftype, ofname)
        q.task_done()


def convertFiles(ifnames : list, nThread : int, iftype: FileType, oftype: FileType, **kwargs):
    q = Queue(ifnames)

