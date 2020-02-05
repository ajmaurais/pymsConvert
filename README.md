# pymsConvert
Convert between common MS data formats.

`pymsConvert` is build on top of [pyopenms](https://pyopenms.readthedocs.io/en/latest/installation.html). 
Custom implementations of file I\O functions not available in `pyopenms`, including `MS2File.store()` are included.
`pymsConvert` is also written to manage and process multiple files in parallel.

## Supported formats
* mzXML
* mzML
* ms2

## Usage
```
usage: main.py [-h] -i {mzXML,mzML,ms2,ms1,mgf} -o {mzXML,mzML,ms2,ms1,mgf}
               [--nThread NTHREAD] [--ofname OFNAME]
               input_file [input_file ...]

Convert between various ms data formats.

positional arguments:
  input_file

optional arguments:
  -h, --help            show this help message and exit
  -i {mzXML,mzML,ms2,ms1,mgf}, --inType {mzXML,mzML,ms2,ms1,mgf}
                        Input file type.
  -o {mzXML,mzML,ms2,ms1,mgf}, --outType {mzXML,mzML,ms2,ms1,mgf}
                        Output file type
  --nThread NTHREAD     Specify number of threads to use. By default, each
                        file is processed in its own thread, up to the number
                        of supported threads on the system.
  --ofname OFNAME       Output file name. Default is input file base name with
                        outType extension.

```
