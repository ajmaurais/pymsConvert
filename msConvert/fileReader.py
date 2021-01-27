
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


def convertFile(ifname : str, iftype: FileType, oftype: FileType, nFractions : int = 1):
    #read input peak map
    peakMap = readToPeakMap(ifname, iftype)

    fileHandeler = _getFileHandeler(oftype)
    if nFractions == 1:
        ofname = '{}.{}'.format(splitext(ifname)[0], oftype.value)
        fileHandeler.store(ofname, peakMap)
    else:
        # get ofnames
        ofnames = list()
        for i in range(nFractions):
            ofnames.append('{}_{}.{}'.format(splitext(ifname)[0], i + 1, oftype.value))

        # get spectra data from peakMap
        peakMap.sortSpectra()
        peakMap.updateRanges()
        msLeveles = peakMap.getMSLevels()
        maxLevel = min(msLeveles)
        spectraList = peakMap.getSpectra()

        nSpectra = len(spectraList)
        beginScan = 0
        endScan = 0
        scansPerFile = nSpectra // nFractions
        scansRemaining = nSpectra % nFractions

        for i, f in enumerate(ofnames):
            # fileHandeler.store(f, peakMap)
            beginScan = endScan
            endScan = beginScan + scansPerFile
            if len(msLeveles) > 1:
                for scan in range(endScan, nSpectra):
                    if spectraList[endScan].getMSLevel() != maxLevel:
                        endScan += 1
                    else:
                        break

            if i == len(ofnames):
                if nSpectra - endScan < scansPerFile:
                    endScan = nSpectra
            print('{} : {} -> {} scans total'.format(beginScan, endScan, endScan - beginScan))
            tempPeakMap = pyopenms.MSExperiment()
            tempPeakMap.setSpectra(spectraList[beginScan:endScan])
            fileHandeler.store(f, tempPeakMap)


def _convertFiles_threadHelper(q : Queue, iftype: FileType, oftype: FileType, **kwargs):
    while True:
        if q.empty():
            break
        item = q.get()
        convertFile(item, iftype, oftype, **kwargs)


def convertFiles(ifnames : list, nThread : int, iftype: FileType, oftype: FileType, **kwargs):
    
    # convertFile(ifnames[0], iftype, oftype, **kwargs)
    
    #init queue of file names
    q = Queue()
    for f in ifnames:
        q.put(f)

    #create thread pool
    threads = [Process(target = _convertFiles_threadHelper,
                       args = [q, iftype, oftype], kwargs = kwargs) for x in range(nThread)]

    for t in threads:
        t.start()

    for t in threads:
        t.join()

