
import pyopenms
import re

class MascotGenericFile(object):
    def store(self):
        raise NotImplementedError('MascotGenericFile store not implemented')

    def load(self, ifname: str, peakMap: pyopenms.MSExperiment):
        inF = open(ifname, 'r')

        lines = inF.read().splitlines()
        curLine = 0
        nLines = len(lines)

        #generate spectrum list
        spectraList = list()
        while curLine < nLines:
            if lines[curLine] == 'BEGIN IONS':
                spectrum = pyopenms.MSSpectrum()
                spectrum.setMSLevel(2)
                precursor = pyopenms.Precursor()

                curLine += 1
                while curLine < nLines:
                    if lines[curLine][0].isalpha():
                        match = re.search('^([A-Z]+)=(.+)$', lines[curLine])
                        if match.group(1) == 'TITLE':
                            titleData = match.group(2).split(',')

                            for s in titleData:
                                if re.search('^scan[_=]', s):
                                    match = re.search('^scan[_=]([0-9]+)', s)
                                    assert(len(match.groups()) == 1)
                                    spectrum.setNativeID('scan={}'.format(match.group(1)))

                        elif match.group(1) == 'PEPMASS':
                            preMZ = [float(x) for x in match.group(2).split(' ')]
                            assert(len(preMZ) <= 2)
                            precursor.setMZ(preMZ[0])
                            if len(preMZ) > 1:
                                precursor.setIntensity(preMZ[1])

                        elif match.group(1) == 'CHARGE':
                            match = re.search('^([0-9])[+-]{0,1}$', match.group(2))
                            assert(len(match.groups()) == 1)
                            precursor.setCharge(int(match.group(1)))

                        elif match.group(1) == 'RTINSECONDS':
                            spectrum.setRT(float(match.group(2)))

                    elif lines[curLine][0].isnumeric():
                        while curLine < nLines and lines[curLine] != 'END IONS':
                            ion = [float(x) for x in lines[curLine].split(' ')]
                            assert(len(ion) == 2)
                            ion_temp = pyopenms.Peak1D()
                            ion_temp.setMZ(ion[0])
                            ion_temp.setIntensity(ion[1])
                            spectrum.push_back(ion_temp)
                            curLine += 1

                        break

                    curLine += 1
                spectrum.setPrecursors([precursor])
                spectraList.append(spectrum)

            curLine += 1

        peakMap.setSpectra(spectraList)


