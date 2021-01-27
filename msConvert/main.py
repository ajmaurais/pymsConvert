
import argparse
import sys
from multiprocessing import cpu_count

from fileTypes import FileType
import fileReader

def getArgs():
    fileTypeList = [val.value for val in FileType.__members__.values()]

    parser = argparse.ArgumentParser(description='Convert between various ms data formats.')

    parser.add_argument('-i', '--inType', choices=fileTypeList, required=True,
                        help='Input file type.')

    parser.add_argument('-o', '--outType', choices=fileTypeList, required=True,
                        help='Output file type')

    parser.add_argument('-s', '--splitFile', type=int, default=1,
                        help='Evenly split the scans in each file into n files.')

    parser.add_argument('--nThread', type=int, default=cpu_count(),
                        help='Specify number of threads to use. '
                             'By default, each file is processed in its own thread, '
                             'up to the number of supported threads on the system.')

    parser.add_argument('input_file', nargs='+')

    args = parser.parse_args()

    args.nThread = args.nThread if len(args.input_file) > args.nThread else len(args.input_file)

    return args


def main():
    args = getArgs()

    fileReader.convertFiles(args.input_file, args.nThread,
                            FileType(args.inType), FileType(args.outType), nFractions=args.splitFile)
    #fileReader.convertFile(args.input_file[0], FileType(args.inType), FileType(args.outType))



if __name__ == '__main__':
    main()

