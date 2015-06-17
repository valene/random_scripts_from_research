#!  /bin/bash
#!  /home/valene/bin

#grab dos and move it to scratch space, in bulk because i am lazy. 

lst=$(ls *.inputdos)
for f in $lst ; do
	dirname="$(echo $f | cut -d'.' -f1)"
	[ -d $dirname ] && echo " $dirname : directory already exists" || mkdir $dirname
done


dir_gen () {
        #generate the directory name 	
	num="$(echo $1 | cut -d'.' -f3 | cut -d'o' -f2)"
	echo "$(echo $1 | cut -d'.' -f1).$num.$hostname"
}

check_dos () {
	#check if the path exist
	FILE_PATH="/scratch/$USER/$(dir_gen $1)/dos"
	#DIR_PATH="/scratch/foo/"
	ssh   $(cat $1) " test -f $FILE_PATH && exit 0 || exit 1 "
}

write_dos () {
	#checks for directory exists and scp files
        if [ -f $1 ] && [ -d $2 ] ; then
	        check_dos $1 && scp $(cat $1):/scratch/$USER/$(dir_gen $1)/* $2/ || echo "Not Found"
        fi
}

for f in $lst ; do
	for i in $(ls $(echo $f | cut -d'.' -f1).sub.o* --sort=time ) ; do
	        out_dir="$(echo $f | cut -d'.' -f1)"
		#check_dos $i && echo "$i and $out_dir use" || echo "skipping $i"
		check_dos $i && write_dos $i $out_dir && echo "skipping $i "
	done
done
