#!/bin/bash
for S in {4..16..2}
do
	echo --- $S
	/bin/time --format='%e s\n%M kB' python nim.py $S
done
