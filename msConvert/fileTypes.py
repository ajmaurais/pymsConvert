
from enum import Enum

class FileType (Enum):
    MZXML = 'mzXML'
    MZML = 'mxML'
    MS2 = 'ms2'
    MS1 = 'ms1'

    @staticmethod
    def getList():
        return [val.value for val in FileType.__members__.values()]