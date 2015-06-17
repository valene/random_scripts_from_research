#! /usr/bin/python
# script to extract from seqquest neb calculation
# output is in xyz form easy for xcrysden visualisation.

import sys, string,math,os,re
bohr2A = 0.52918
R2E = 13.605

try : 
  inputfilename = sys.argv[1]
except :
  print ("Seqquest NEB output file needed!")
  raise SystemExit

inputfile = open(inputfilename,"r")
outfilename = string.split(inputfilename,".")[0] + "_neb.xyz"
print ("outfile name", outfilename)
outfile = open(outfilename,"w")
nebfilename = string.split(inputfilename,".")[0] + ".neb_geom"
nebfile = open(nebfilename, "r")
posfilename = string.split(inputfilename,".")[0] + ".neb_post"
postfile = open(posfilename,"r")

inp0 = inputfile.readlines()
inpneb = nebfile.readlines()
postinp = postfile.readlines()

#Optional dictionaries
atomtypedict={"Pt.atm":"Pt","o_tm.atm":"O","Pd.atm":"Pd","h_ae.atm":"H","f_tm.atm":"F",
		"N.atm":"N","C.atm":"C", "S.atm":"S", "Au.atm":"Au","O.atm":"O","na.atm":"Na",
	      "pt_pbe.atm":"Pt","si.atm":"Si","Li_hard.atm":"Li","Li.atm":"Li","V.atm":"V"}
atomtypes=[]
atomarray=[]
enerarray=[]

#read initial atom types from .out or .in files
lflag = 0
coordblock = []
for idx,lin in enumerate(inp0):
	if "number" in lin and "of" in lin and "atoms" in lin:
		natoms = int(string.split(inp0[idx + 1])[0])
	if "atom file" == lin.strip() :
	       atomtypes.append(atomtypedict[string.split(inp0[idx+1])[0]])
	if "atom" in lin and "type" in lin and "position" in lin and lflag == 0:
		coordblock = inp0[idx+1:idx+natoms+1]
		lflag = 1
		for coordlin in coordblock:
			#atomarray.append(int(string.split(coordlin)[1]))
                        atomarray.append(atomtypes[int(string.split(coordlin)[1])-1]) 
                        #USE one of the above, first one of number and second for atom symbol
	continue

	

#read initial and final energies from .neb_post file
enerblock = []
for idx, lin in enumerate(postinp):
     if "Img" in lin and "distance" in lin:
         enerblock = postinp[idx+1:]
for enerlin in enerblock:
   enerarray.append(float(string.split(enerlin)[2]))

print (enerarray[0])

img = 0
ini_geom = []
fin_geom = []
img_geom = []
#read geomertries from .neb_geom file
for idx, lin in enumerate(inpneb):
     if "coordinate" in lin and "start-point" in lin:
         ini_geom = inpneb[idx+1:idx+natoms+1]
	 outfile.write("%d \n" % (natoms))
         outfile.write("Initial structure %2.6f" % (R2E*enerarray[0]))
	 #outfile.write(''.join(ini_geom))
	 for idx2, i in enumerate(ini_geom):
		 outfile.write("\n %s \t %2.8f \t %2.8f \t %2.8f" % (atomarray[idx2],bohr2A*float(str.split(i)[0]),bohr2A*float(str.split(i)[1]),bohr2A*float(str.split(i)[2])))
     if "coordinate" in lin and "image" in lin:
        img = img + 1
     	img_geom = inpneb[idx+1:idx+natoms+1]
        outfile.write("\n%s \n" % (natoms))
	outfile.write("%2.6f" % (R2E*enerarray[img]))
	#outfile.write(''.join(img_geom))
	for idx2, i in enumerate(img_geom):
		 outfile.write("\n %s \t %2.8f \t %2.8f \t %2.8f" % (atomarray[idx2],bohr2A*float(str.split(i)[0]),bohr2A*float(str.split(i)[1]),bohr2A*float(str.split(i)[2])))
     if "coordinate" in lin and "end-product" in lin:
         fin_geom = inpneb[idx+1:idx+natoms+1]
	 #outfile.write("Final Structure \n")
	 #outfile.write("%2.6f \n" % (enerarray[-1]))
	 #outfile.write(''.join(fin_geom))
     continue	

outfile.write("\n%s \n" % (natoms))
outfile.write("%2.6f" % (R2E*enerarray[-1]))
for idx2, i in enumerate(fin_geom):
	outfile.write("\n %s \t %2.8f \t %2.8f \t %2.8f" % (atomarray[idx2], bohr2A*float(str.split(i)[0]),bohr2A*float(str.split(i)[1]),bohr2A*float(str.split(i)[2])))



inputfile.close()
outfile.close()
nebfile.close()
postfile.close()
