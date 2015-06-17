#! /usr/bin/python
#script takes a bulk structure in *.xyz and slices pieces of molecules
#slice is done with a random number generated origin and user defined radius

# TO DO: define uniqueness criterion for selecting structures


import sys,string,math,os,re,random

#Load input file
try:
   inputfilename = sys.argv[1]
except:
   print "Input data file missing"
   raise SystemExit

#opening the input and output files
inpfile = open(inputfilename,"r")

#read input file and store atom positions
inp0 = inpfile.readlines()
n = len(inp0)
num_atoms = int(string.split(inp0[0])[0])
print "number of atoms in bulk structure :", num_atoms
a0 = []
x0 = []
y0 = []
z0 = []
for line in range(2,n):
        a0.append(string.split(inp0[line])[0])
        x0.append(float(string.split(inp0[line])[1]))
        y0.append(float(string.split(inp0[line])[2]))
        z0.append(float(string.split(inp0[line])[3]))

#close input file
inpfile.close()

#obtain radius for slicing sphere
nb = input('Enter the radius in Angstrom')
try:
   rad0	= float(nb)
except:
   print "Integer or Floating point number needed"
   raise SystemExit

for i in range(50):
    #i0 = random.choice(range(num_atoms))
    xr0 = random.uniform(min(x0),max(x0))
    yr0 = random.uniform(min(y0),max(y0))
    zr0 = random.uniform(min(z0),max(z0))
    selectatoms = []
    shiftatoms = []
    #selecting atoms within the sphere
    for j in range(num_atoms):
	    if math.sqrt((x0[j] - xr0)**2 + (y0[j] - yr0)**2 + (z0[j] - zr0)**2) <= rad0:
	          selectatoms.append(str(a0[j]) + str.rjust("%.6f" % (x0[j]),12)  + str.rjust("%.6f" %(y0[j]),10)	+ str.rjust("%.6f" % (z0[j]),10)) 
		  continue
    #end of atoms selection
    #begin of shifting of origin the selected structures
    for k in range(len(selectatoms)):
            shiftatoms.append(string.split(selectatoms[k])[0] +  str.rjust("%.6f" % (float(string.split(selectatoms[k])[1]) - float(string.split(selectatoms[0])[1])),10) + str.rjust("%.6f" % (float(string.split(selectatoms[k])[2]) - float(string.split(selectatoms[0])[2])),8) + str.rjust("%.6f" % (float(string.split(selectatoms[k])[3]) - float(string.split(selectatoms[0])[3])),10))
    #end of origin shift for structures	    
    with open (string.split(inputfilename,".")[0] + "_sliced%i.xyz"  %i, 'w') as f:
         f.write('%i \n \n' % (len(selectatoms)))
         f.write("\n".join(selectatoms))
    print "\n", len(selectatoms)
    print "\n"
    print selectatoms

