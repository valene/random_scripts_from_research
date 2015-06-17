#! /usr/bin/env python2
# this script converts SeqQuest input or output to a xyz-file
# usage: thisscriptname <SeqQuestfilename> <x-periodicity> <y-periodicity> <z-periodicity>  
#original script was of Jochen , I believe.
#NOTE: modified to account for an access bug in the lists.

import sys,string,math, os,re
#A2bohr = 1.0 / 0.5291772108
#bohr2A = 0.5291772108
A2bohr = 1.0/0.52918
bohr2A = 0.52918


# check arguments
try :
   inputfilename = sys.argv[1]
except :
    print "seqquest input/output file is missing!"
    raise SystemExit
try:
     periodicity   = [ int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) ]
except:
     print "no proper arguments for periodicity are given, using default values 1 1 1 "
     periodicity  = [1, 1, 1]
     
#open input and output files
inputfile = open(inputfilename,"r")
bsoutputfilename = string.split(inputfilename, ".")[0] + "xbs.bs"
print "bsoutputfilename", bsoutputfilename
bsoutfile = open(bsoutputfilename,"w")
mvoutputfilename = string.split(inputfilename, ".")[0] + "xbs.mv"
print "mvoutputfilename", mvoutputfilename
mvoutfile = open(mvoutputfilename,"w")
xyzoutputfilename = string.split(inputfilename, ".")[0] + ".xyz"
print "xyzoutputfilename", xyzoutputfilename
xyzoutfile = open(xyzoutputfilename,"w")
xyzmovfilename = string.split(inputfilename,".")[0] + ".full.xyz"
print "xyzmoviefilename", xyzmovfilename
xyzmovfile = open(xyzmovfilename,"w")

#initialize some variables
geometrycount = 0
latticeflag=0
bsfileflag=1

# dictionary and list for atomfiles
atomtypedict={"Pt.atm":"Pt","o_tm.atm":"O","Pd.atm":"Pd","h_ae.atm":"H","f_tm.atm":"F",
		"N.atm":"N","C.atm":"C", "S.atm":"S", "Au.atm":"Au","O.atm":"O","na.atm":"Na",
	      "pt_pbe.atm":"Pt","si.atm":"Si","Li_hard.atm":"Li","Li.atm":"Li","V.atm":"V"}
atomtypes=[]
xyzcell=[]
xyzfullcell=[]

# loop over lines if inputfile
input = inputfile.readlines()
n = len(input)
for line in range(n):
     # check dimension
     if "dimension" in input[line] and  "of" in input[line] and  "system" in input[line]:
         #linenumber=input.index(line)
         if ("0" in input[line +1] or "1" in input[line +1] ):
             print "sorry, I cannot treat systems with dimension: ", input[line +1]
             #raise SystemExit
	     dimension = str.strip(input[line +1])
         else:
            dimension = str.strip(input[line +1])
         continue
     # check Lattice coordinates
     if "coordinates" in input[line]:
         #linenumber=input.index(line)
         if ("LATTICE" in input[line +1] ):
         #    print "sorry, I can only treat systems with LATTICE coordinates "
         #    raise SystemExit
           latticeflag = 1
         continue
     #get cell parameters
     if "primitive" in input[line] and "lattice" in input[line] and "vectors" in input[line]:
         #linenumber=input.index(line)
         print line
	 try:
           latticex = map(lambda x : float(string.strip(x)),str.split(input[line + 1]))
	 except:
           latticex = map(lambda x : float(string.strip(x)),[input[line + 1][0:13],input[line + 1][13:25],input[line + 1][25:37]])
	 print "x lattice vector",  latticex 
         try:
           latticey = map(lambda x : float(string.strip(x)),str.split(input[line + 2]))
         except:
           latticey = map(lambda x : float(string.strip(x)),[input[line + 2][0:13],input[line + 2][13:25],input[line + 2][25:37]])
         print "y lattice vector",  latticey
         try:
           latticez = map(lambda x : float(string.strip(x)),str.split(input[line + 3]))
         except:
           latticez = map(lambda x : float(string.strip(x)),[input[line + 3][0:13],input[line + 3][13:25],input[line + 3][25:37]])
         print "z lattice vector",  latticez
         continue
     #get number of atoms
     if "number" in input[line] and "of" in input[line] and "atoms" in input[line]:
         #linenumber=input.index(line)
         numberofatoms = int(string.split(input[line +1])[0])
         print "number of atoms: " ,  numberofatoms
         #xyzoutfile.write('%3i \n' % (numberofatoms))
	 xyzoutfile.write(str(numberofatoms) + "\n")
	 xyzoutfile.write('\n')
	 continue
     # get atoms types
#     if "atom types" == line.strip() :
     if input[line].strip()  == "atom file" :
        print "\n atom file type found"
     if "atom file" == input[line].strip() :
         #linenumber=input.index(line)
         # someone should fix this bug
         #atomtypesnumber=int(input[linenumber +1])
         #for atomtype in range(atomtypesnumber):
         #  atomtypelinenumber=atomtype*2+2+linenumber
         #  atomtypes.append(atomtypedict[string.split(input[atomtypelinenumber +1])[0]])
         atomtypes.append(atomtypedict[string.split(input[line +1])[0]])
         print "atomtypes: ", atomtypes
	 continue
     # get coordinates
     if "atom," in input[line] and  "type," in input[line] and "position" in input[line]:
         #linenumber=input.index(line)
         geometrycount = geometrycount + 1
         print "Found new geometry",  geometrycount
	 print line
	 # print caption to mv-file
         xyzfullcell.append(str(numberofatoms) + "\n")
         xyzfullcell.append("\n")
         #prepares atomnumber and blank space for xyz format
         if not bsfileflag:
             mvoutfile.write("frame:   " + str(geometrycount ) +"\n")
         # get atomcoordinates section and convert coordinates
         coordinates = input[line+1:line + numberofatoms+1]
         # prepare some lists
         unitcell=[]
         othercells=[]
	 for coordline in coordinates:
             #atomname = "atom   cl" + string.split(coordline)[1]
             atomname = atomtypes[int(string.split(coordline)[1]) -1]
             #print atomname
             #calculate coordinates
             if latticeflag and dimension=="3":
               xcoordorg = ( latticex[0] * float(string.split(coordline)[2]) + latticey[0] * float(string.split(coordline)[3]) + latticez[0] * float(string.split(coordline)[4])  ) 
               ycoordorg = ( latticex[1] * float(string.split(coordline)[2]) + latticey[1] * float(string.split(coordline)[3])   + latticez[1] * float(string.split(coordline)[4])  ) 
               zcoordorg = ( latticex[2] * float(string.split(coordline)[2]) + latticey[2] * float(string.split(coordline)[3])   + latticez[2] * float(string.split(coordline)[4])  ) 
             if latticeflag and dimension=="2":
               # treat z-direction in a special way in slab calculations
               xcoordorg = ( latticex[0] * float(string.split(coordline)[2]) + latticey[0] * float(string.split(coordline)[3])  + latticez[0] * float(string.split(coordline)[4])  ) 
               ycoordorg = ( latticex[1] * float(string.split(coordline)[2]) + latticey[1] * float(string.split(coordline)[3])  + latticez[1] * float(string.split(coordline)[4])  ) 
               zcoordorg = float(string.split(coordline)[4])
               # everything is easy with cartesian coordinates
             if not latticeflag:
               xcoordorg = float(string.split(coordline)[2])
               ycoordorg = float(string.split(coordline)[3])
               zcoordorg = float(string.split(coordline)[4])

             # add atoms in neighbor cells
             for px in range(periodicity[0]):
                 for py in range(periodicity[1]):
                     for pz in range(periodicity[2]):
                         xcoord = xcoordorg + latticex[0] * px + latticey[0]  * py + latticez[0]  * pz
                         ycoord = ycoordorg + latticex[1] * px + latticey[1]  * py + latticez[1]  * pz
                         zcoord = zcoordorg + latticex[2] * px + latticey[2]  * py + latticez[2]  * pz
                             # to get correct labelling, treat everything with periodicity (0,0,0) in a special way
                         if (px,py,pz) == (0,0,0):
                             xyzfullcell.append(atomname + str.rjust("%.8f" %(xcoord*bohr2A),15) + str.rjust("%.8f" %(ycoord* bohr2A), 13) +str.rjust("%.8f" %(zcoord* bohr2A), 13) + "\n")
                             if bsfileflag:
                                unitcell.append(atomname + str.rjust("%.8f" %(xcoord*bohr2A), 15) + str.rjust("%.8f" %(ycoord* bohr2A), 13) + str.rjust("%.8f" %(zcoord* bohr2A), 13) + " \n" )
                                xyzcell.append(atomname )
			     else:
                                unitcell.append(str.rjust("%.8f" %(xcoord*bohr2A), 15) + str.rjust("%.8f" %(ycoord* bohr2A), 13) + str.rjust("%.8f" %(zcoord* bohr2A), 13) + " \n" )
		         else:
                             xyzfullcell.append(atomname + str.rjust("%.8f" %(xcoord*bohr2A),15)+ str.rjust("%.8f" %(ycoord*bohr2A), 13) + str.rjust("%.8f" %(zcoord* bohr2A), 13) + "\n")
			     if bsfileflag:
                                 othercells.append( atomname + str.rjust("%.8f" %(xcoord*bohr2A), 15) + str.rjust("%.8f" %(ycoord* bohr2A), 13) + str.rjust("%.8f" %(zcoord* bohr2A), 13) + " \n" )
                                 xyzcell.append(atomname)
			     else:
                                 othercells.append( str.rjust("%.8f" %(xcoord*bohr2A), 15) + str.rjust("%.8f" %(ycoord* bohr2A), 13) + str.rjust("%.8f" %(zcoord* bohr2A), 13) + " \n" )
	 #write first coordinates to bsfile, all other to mv file (in Angstrom units)
         #xyzoutfile.writelines(xyzcell)
	 
	 if bsfileflag:
           bsoutfile.writelines(unitcell)
           bsoutfile.writelines(othercells)
         else:
           mvoutfile.writelines(unitcell)
           mvoutfile.writelines(othercells)
         # after first geometry is written, change flag
         bsfileflag = 0
	 continue
#write footer to bsoutfile
bsoutfile.write(    "\n  "
+  "\n  "
+  "spec     cl1      1.400   0.80 0.8  0.8 \n  "
+  "spec     cl2      1.400   1.0  0.2  0.2 \n  "
+  "spec     cl3      1.400   0.25 1.00 0.25 \n "
+  "spec     cl4      1.400   0.3  0.3  1.0 \n "
+  "spec     cl5      1.400   0.35 0.35 0.35 \n "
+  "spec     cl6      1.400   0.4  0.4  0.4 \n "
+  "spec     cl7      1.400   0.45 0.45 0.45 \n "
+  "spec     cl8      1.400   0.5  0.5  0.5 \n "
+  "spec     cl9      1.400   0.65 0.65 0.65 \n "
+  "spec     cl10     1.400   0.8  0.8  0.8 \n "
+  "spec     cl11     1.400   0.95 0.95 0.95 \n "
+  "spec     cl12     0.800   1.0  0.2  0.0 \n "
+  "spec  cleck      1.000   0.80  0.40 0 \n "
+  "spec   hard      1.000   0.8  0.8 0.0 \n  "
+  "spec hardeck      1.000   0.8  0.8 0.0 \n "
+  "spec   soft                       1.000   0.0  0.95 0.4 \n " 
+  "spec softeck      1.000   0.0  0.95 0.4   \n " 
+  "\n "
+  "bonds    cl1    cl1    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl2    cl2    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl3    cl3    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl4    cl4    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl5    cl5    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl6    cl6    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl7    cl7    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl8    cl8    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl9    cl9    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl10   cl10   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl11   cl11   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl12   cl12   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl1    cl2    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl1    cl3    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl1    cl5    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl1    cl9    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl5    cl9    0.000    3.000    0.090   1.0 \n "
+  "bonds    cl2    cl3    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl3    cl4    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl4    cl5    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl5    cl6    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl6    cl7    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl7    cl8    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl8    cl9    0.000    4.000    0.090   1.0 \n "
+  "bonds    cl9    cl10   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl10   cl11   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl11   cl12   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl10   cl12   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl9    cl12   0.000    4.000    0.090   1.0 \n "
+  "bonds    cl8    cl12   0.000    4.000    0.090   1.0 \n "
+  " \n "
+  "tmat -0.014  1.000  0.000 -0.492 -0.007  0.871  0.871  0.012  0.494 \n "
+  "dist    42.514 \n "
+  "inc      5.000 \n "
+  "scale    7.158 \n "
+  "rfac 0.80 \n "
+  "bfac 3.00 \n "
+  "pos    0.000    0.000 \n "
+  "switches 1 0 1 0 0 1 1 2 0 \n "
+  "\n "
)

#write the complete movie file in xyz format
xyzmovfile.writelines(xyzfullcell)

mvoutfile.close()
mvoutfile = open(mvoutputfilename,"r+")

#extract last frame and add it to .xyz file
mvinput =  mvoutfile.readlines()
mvn = len(mvinput)
mergedcell = []
for i in range(mvn-numberofatoms*periodicity[0]*periodicity[1]*periodicity[2],mvn):
	#print xyzcell[i-mvn+numberofatoms*periodicity[0]*periodicity[1]*periodicity[2]]
	mergedcell.append(xyzcell[i-mvn+numberofatoms*periodicity[0]*periodicity[1]*periodicity[2]] + mvinput[i])
xyzoutfile.writelines(mergedcell)


# close fies
inputfile.close()
bsoutfile.close()
mvoutfile.close()
xyzoutfile.close()
xyzmovfile.close()

