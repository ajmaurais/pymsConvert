
import argparse
import sys
from multiprocessing import cpu_count

from fileTypes import FileType

def getArgs():
    fileTypeList = [val.value for val in FileType.__members__.values()]

    parser = argparse.ArgumentParser(description='Convert between various ms data formats.')

    parser.add_argument('-i', '--inType', choices=fileTypeList, required=True,
                        help='Input file type.')

    parser.add_argument('-o', '--outType', choices=fileTypeList, required=True,
                        help='Output file type')

    parser.add_argument('--nThread', type=int, default=cpu_count(),
                        help='Specify number of threads to use.'
                             'By default, each file is processed in its own thread,'
                             'up to the number of supported threads on the system.')

    parser.add_argument('--ofname',
                        help='Output file name. Default is input file base name with outType extension.')

    parser.add_argument('input_file', nargs='+')

    args = parser.parse_args()

    # manually check args
    if len(args.input_file) > 1 and args.ofname is not None:
        sys.stderr.write('Error! Can not specify OFNAME if multiple inputs are given!\n')
        exit(-1)

    return args


def main():
    args = getArgs()




if __name__ == '__main__':
    main()

