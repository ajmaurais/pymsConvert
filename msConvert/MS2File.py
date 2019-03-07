
import re
import datetime
from os.path import basename
import pyopenms

class MS2File(pyopenms.MS2File):

    _h_tag = 'H'
    _s_tag = 'S'
    _i_tag = 'I'
    _z_tag = 'Z'
    _ion_sep = ' '
    _H_mass = 1.00783
    _activationMethods = ["CID", "PSD", "PD", "SID", "BIRD", "ECD",
                          "IMD", "SORI", "HCID", "LCID", "PHD", "ETD", "PQD"]

    def _getScan(self, nativeIDStr : str) -> str:
        m = re.search('scan=([0-9]+)', nativeIDStr)
        return m.group(1)


    def _writeValue(self, tag, name, value, newLine = True):
        ret = '{}\t{}\t{}'.format(tag, name, value)
        if newLine:
            ret += '\n'
        return ret


    def store(self, ofname: str, peakMap : pyopenms.MSExperiment):

        #sort peakMap if necessary
        if not peakMap.isSorted():
            peakMap.sortSpectra()
            peakMap.updateRanges()

        outF = open(ofname, 'w')

        firstScan = self._getScan(peakMap.getSpectrum(0).getNativeID().decode('utf-8'))
        dataType = peakMap.getSpectrum(0).getType()
        dataType = 'Centroid' if dataType == 1 else 'Profile' if dataType == 2 else 'Unknown'
        lastScan = self._getScan(peakMap.getSpectrum(peakMap.getNrSpectra() - 1).getNativeID().decode('utf-8'))
        precursorFile = basename(ofname).replace('ms2', 'ms1')

        #print header
        outF.write(self._writeValue(MS2File._h_tag, 'CreationDate',
                                    datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')))
        outF.write(self._writeValue(MS2File._h_tag, 'Extractor', 'msConvert'))
        outF.write(self._writeValue(MS2File._h_tag, 'ExtractorVersion', '0.1'))
        outF.write(self._writeValue(MS2File._h_tag, 'Comments',
                                    'msConvert was written by Aaron Maurais, 2019'))
        outF.write(self._writeValue(MS2File._h_tag, 'ExtractorOptions', 'MS2'))
        outF.write(self._writeValue(MS2File._h_tag, 'AcquisitionMethod', 'Data-Dependent'))
        outF.write(self._writeValue(MS2File._h_tag, 'InstrumentType', 'Unknown'))
        outF.write(self._writeValue(MS2File._h_tag, 'ScanType', 'MS2'))
        outF.write(self._writeValue(MS2File._h_tag, 'DataType', dataType))
        outF.write(self._writeValue(MS2File._h_tag, 'FirstScan', firstScan))
        outF.write(self._writeValue(MS2File._h_tag, 'LastScan', lastScan))

        #iterate through spectra
        preScan = 'Unknown'
        for i, scan in enumerate(peakMap.getSpectra()):
            if scan.getMSLevel() == 1:
                preScan = self._getScan(scan.getNativeID().decode('utf-8'))

            if scan.getMSLevel() == 2:
                #write header info
                curScan = self._getScan(scan.getNativeID().decode('utf-8'))
                precursors = scan.getPrecursors()
                preCharge = int(precursors[0].getCharge())
                preMZ = precursors[0].getMZ()


                #print scan line
                outF.write('{}\t{}\t{}\t{}\n'.format(MS2File._s_tag,
                                                    curScan.zfill(6),
                                                    curScan.zfill(6),
                                                    preMZ))
                #print scan info
                outF.write(self._writeValue(MS2File._i_tag, 'RetTime', scan.getRT()))
                outF.write(self._writeValue(MS2File._i_tag, 'PrecursorInt',
                                            precursors[0].getIntensity()))
                outF.write(self._writeValue(MS2File._i_tag, 'IonInjectionTime', 'Unknown'))
                ameth = list(precursors[0].getActivationMethods())
                ameth = ' '.join([MS2File._activationMethods[x] for x in ameth])
                outF.write(self._writeValue(MS2File._i_tag, 'ActivationType', ameth))
                outF.write(self._writeValue(MS2File._i_tag, 'PrecursorFile', precursorFile))
                outF.write(self._writeValue(MS2File._i_tag, 'PrecursorScan', preScan))
                outF.write(self._writeValue(MS2File._i_tag, 'InstrumentType', 'Unknown'))

                #write z line
                #after charge, the M+H m/z for the ion is listed, so calculate that here
                outF.write(self._writeValue(MS2File._z_tag, preCharge,
                                            (float(preMZ) * preCharge) -
                                            (preCharge * MS2File._H_mass) + MS2File._H_mass))

                #write ions
                for ion in scan:
                    outF.write('{0:.4f} {0:.1f}\n'.format(round(ion.getMZ(),4),
                                                    round(ion.getIntensity(), 1)))



