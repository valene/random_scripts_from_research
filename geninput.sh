#! /bin/bash
#! /bin/usr/perl

#copy ccoordinates from a converged output file to input file
#usage: script.sh file1.out file2.in

#perl -ne 'if (/atom, type/../kgrid/) { /\./ ? next : print $_ } else {print $_}' $1
perl -e '$/=undef; $f=<>; push @a,$1 while($f=~m#FINAL GEOMETRY(.*?)FINAL RELAXED#msg); print $a[-1]' $1 | grep '\.' > temp.dat
perl -ne 'print if 1 .. m(atom, type)' $2 > $2_part1.txt
perl -ne 'print if m(kgrid) .. -1' $2 > $2_part2.txt
cat $2_part1.txt temp.dat $2_part2.txt > $2 && rm -rf temp.dat $2_part1.txt $2_part2.txt 
