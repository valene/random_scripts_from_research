#! /usr/bin/python
#testing script for principal component analysis

import sys,string,math,os,re
import identify_unique

#Load Input file
#just cat various .xyz files

try:
   inputfilename = sys.argv[1]
except:
   print "Input data file missing"
   raise SystemExit

inpfile = open(inputfilename,"r")
inp0 = inpfile.readlines()
n = len(inp0)
inpfile.close()

structs=[]
i = 0

for idx, x in enumerate(inp0):
	tempstruct = []
	if len(x) == 1:
	  try:
		i0 = int(inp0[idx-1])
		print i0
		tempstruct = inp0[idx+1:idx+1+i0]
		#print len(tempstruct)
          except ValueError:
		continue
          structs.append(tempstruct)


print 'xxxxxxxxxxxxxxxxxxx\n', len(structs)
print 'read input structure is ', structs[0]
rest_struct = identify_unique.struct_unique(structs)

outputfile = string.split(inputfilename,".")[0] + "individual.xyz"
outfile = open(outputfile,"w")
for x in rest_struct:
	outfile.write("%i \n" % (len(x)))
	for y in x:
		outfile.write("\n %s \t %2.8f  \t %2.8f \t %2.8f \t %2.8f \t %2.8f " % (y[0], y[1], y[2], y[3], y[4], y[5]))
        outfile.write("\n")		
outfile.close()		
