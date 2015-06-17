#! /usr/bin/python
#python code to shift origin for charged state calculation

import sys,string,math,os,re

try : 
   inputfilename = sys.argv[1]
except :
   print "input file missing!"
   raise SystemExit

inputfile = open(inputfilename,"r")
outputfilename = string.split(inputfilename, ".")[0] + "shifted.xyz"
outputfile = open(outputfilename,"w")

input = inputfile.readlines()
n = len(input)
outputfile.writelines(input[0])
outputfile.writelines(input[1])

sx = float(input[2].split()[1])
sy = float(input[2].split()[2])
sz = float(input[2].split()[3])
for line in range(n-2):
     l2 = line + 2
     atype = str.strip(input[l2])[0]
     ax = float(input[l2].split()[1])
     ay = float(input[l2].split()[2])
     az = float(input[l2].split()[3])
     outputfile.write( atype + '\t %10.5f \t %10.5f \t %10.5f \n'  % (ax-sx, ay-sy, az-sz))
inputfile.close()
outputfile.close()
