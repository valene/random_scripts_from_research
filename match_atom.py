#! /usr/bin/python
#module to select structures with specified number of atomic species.

def struct_select(structlist):
     sub0 = "Li"	
     n = len(structlist)
     selectlist = []
     for i in range(n):
	 count = 0    
         for j in range(len(structlist[i])):
	     count = count + structlist[i][j].count(sub0)
	 if count%2 == 0:
            selectlist.append(structlist[i])
     print "\n", len(selectlist)	    
     return selectlist;	    
