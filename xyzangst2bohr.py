#! /usr/bin/python
#code converts xyz files in angstrom to bohr 

import math,sys,string

try:
  inname = sys.argv[1]
except:
  print "file required"
  raise SystemExit

infile = open(inname,"r")
outname = string.split(inname,".")[0] + "_in_bohr.xyz"
outfile = open(outname,"w")


j1=[]
j2=[]
j3=[]
j4=[]
b=infile.readlines()
bn = len(b)
for i in range(bn-2):
	j1.append(str(b[i+2].split()[0]))
	j2.append(float(b[i+2].split()[1]))
	j3.append(float(b[i+2].split()[2]))
	j4.append(float(b[i+2].split()[3]))
n=len(j1)
s1 = 1.0/0.52918

outfile.write(b[0])
outfile.write('\n')

for i in range(n):
     outfile.write('%s  \t %10.10f \t %10.10f \t %10.10f \n' % (j1[i], s1*j2[i],s1*j3[i],s1*j4[i]))
infile.close()
outfile.close()
