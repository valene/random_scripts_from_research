#! /bin/bash

#Another brutal hack to just bulk get structure from whole directories.

atomno () { perl -lane 'if (m/cell$/../^atom/g and m/^\W/) { my $a = $_ ; $a =~ s/^\s+//; print $a} ; ' $1 ;}
coords () { perl -lane 'if (m/position vector/../kgrid2/g and m/^\W/) {my $s = 0.529 ; @F = split(" ", $_ ); ($F[1] == '1')? print "O \t ", $s*$F[2] ,  " \t ",  $s*$F[3], " \t " , $s*$F[4] : print "C \t ", $s*$F[2], " \t ", $s*$F[3], " \t ", $s*$F[4] ; } ' $1 ; }
energy () { perl -lane ' if (m/FINAL RELAXED/g) {print sprintf("%3.3f", $F[-1]) }' $1 ; } 

#atomno $1
#energy 
#coords $1

for f in $(ls *.in)
do
    a=`echo $f | cut -d'.' -f1`
    for o in $(ls ../*.out)
    do
	b=`echo $o | cut -d'/' -f2 | cut -d'.' -f1 | cut -d'-' -f1`
	if [ "$a" == "$b" ] && [ -n "$(echo `energy $o`)" ]
	then
	    atomno $f >> collect.xyz
	    energy $o >> collect.xyz
            coords $f >> collect.xyz
        fi
    done
done
