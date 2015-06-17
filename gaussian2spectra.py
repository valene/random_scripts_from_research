#! /usr/bin/python
# script to extract spectra from gaussian out files.

import sys,string,math,os,re



#Lorentzian 
def  lrntz(z,a,b,c):
     return (b*c*c)/((z-a)*(z-a) + c*c)

#gaussian
def gssn(z,a,b,c):
    return b*math.exp(-1*(z-a)*(z-a)/(2*c*c))


try :
   inputfilename = sys.argv[1]
except :
    print "Required a gaussian Output file!"
    raise SystemExit

#open input and output files
inputfile = open(inputfilename,"r")
specfilename = string.split(inputfilename, ".")[0] + ".dat"
specfile = open(specfilename,"w")

inp = inputfile.readlines()


#inc =4 for raman spectra and 3 for IR
#brd is broadening factor and sf is scale factor
inc = 4
brd = 1.5
sf = 0.9614

for idx, line in enumerate(inp):
     if "Harmonic" in line and "frequencies" in line:
	rin = []
     if "Frequencies" in line  and str.split(line)[0] == "Frequencies" :
	     freq1 = [float(str.split(inp[idx])[2]),float(str.split(inp[idx+inc])[3])]
	     freq2 = [float(str.split(inp[idx])[3]),float(str.split(inp[idx+inc])[4])]
	     freq3 = [float(str.split(inp[idx])[4]),float(str.split(inp[idx+inc])[5])]
	     rin.append(freq1)
	     rin.append(freq2)
	     rin.append(freq3)

spectra = []
fq = []
atv = []
for i in range(len(rin)):
     for j in range(8000):
	  fq.append(-0.005*4000 + 0.05*j + rin[i][0])

for x in fq:
    y = 0.0
    for k in rin:
	y = y + lrntz(x,k[0],k[1],brd)
    atv.append(y)
    spectra.append([sf*x,y])
    spectra.sort(key=lambda l:l[0])




for i in range(len(spectra)):
	specfile.write("%2.8f \t %2.8f \n" % (spectra[i][0], spectra[i][1]))

inputfile.close()
specfile.close()
