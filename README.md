# msConvert
Convert between common MS data formats.

`msConvert` is build on top of [pyopenms](https://pyopenms.readthedocs.io/en/latest/installation.html). 
Custom implementations of file I\O functions not available in `pyopenms`, including `MS2File.store()` and `MascotGenericFile.load()` are also included.
`msConvert` is also written to manage and process multiple files in parallel.

## Supported formats
* mzXML
* mzML
* ms2

## Dependencies
```
pyopenms
```
