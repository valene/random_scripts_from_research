#! /usr/bin/python
# script to perform boltzmann averaging over conformers
# requires the spectra of conformers and an energy source file sort accordingly

import sys,string,math,os,re
import scipy,numpy,scipy.interpolate

#defining boltzman factor
def btlz(ener,temp):
    return math.exp(-1*ener/temp)

try :
   inputfilename = sys.argv[1]
except :
   print "Required a filename with spectrafiles and energies"
   raise SystemExit

inputfile = open(inputfilename,"r")


inp = inputfile.readlines()

enarr = []
ifarr = []
fact = []
for l in inp:
     ifarr.append(str.split(l)[0])
     enarr.append(float(str.split(l)[1]))

temp = 0.02569  #298.15 in kelvin

en0 = min(enarr)
nfsum= 0
for idx, s in enumerate(enarr):
	enarr[idx]= s-en0
        fact.append(btlz(s-en0, temp))
        nfsum = nfsum + fact[idx]

for idx, s in enumerate(fact):
	fact[idx] = fact[idx]/nfsum

print fact

x_new = numpy.linspace(0,800,20000)
spec_avg = numpy.zeros(20000)
for idx, s in enumerate(ifarr):
	datfile = open(ifarr[idx],"r")
	dat0 = datfile.readlines()
	x0 = []
	y0 = []
	for lin in dat0:
		x0.append(float(str.split(lin)[0]))
		y0.append(float(str.split(lin)[1]))
        intplt3 = scipy.interpolate.interp1d(x0,y0,kind='linear')
	y_new = intplt3(x_new)
        y_new.tolist()
        for i in range(len(y_new)):
		spec_avg[i] = spec_avg[i] + fact[idx]*y_new[i]
        datfile.close()

with open ("averagedspectra.dat", 'w') as f:
     for i in range(len(x_new)):
	     f.write("%2.8f \t %2.8f \n" % (x_new[i],spec_avg[i]))


inputfile.close()


