
from os.path import splitext
from multiprocessing import Process, Queue
import pyopenms

from fileTypes import FileType
from MS2File import MS2File
from mascotGenericFile import MascotGenericFile


def _getFileHandeler(iftype: FileType):
    if iftype == FileType.MZML:
        return pyopenms.MzMLFile()
    elif iftype == FileType.MZXML:
        return pyopenms.MzXMLFile()
    elif iftype == FileType.MS2:
        return MS2File()
    elif iftype == FileType.MGF:
        return MascotGenericFile()
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
        if q.empty():
            break
        item = q.get()
        convertFile(item, iftype, oftype, ofname)
        #q.task_done()


def convertFiles(ifnames : list, nThread : int, iftype: FileType, oftype: FileType, **kwargs):

    _ofname = None if 'ofname' not in kwargs else kwargs['ofname']

    #init queue of file names
    q = Queue()
    for f in ifnames:
        q.put(f)

    #create thread pool
    threads = [Process(target = _convertFiles_threadHelper,
                       args = [q, iftype, oftype, _ofname]) for x in range(nThread)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
