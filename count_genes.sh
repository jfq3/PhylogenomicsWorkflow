#!/bin/bash
# Count ribo genes found
rm num_genes.txt
for f in $(ls *.tbl)
do
	num=$(egrep -c '(RpL|RpS)' $f)
	bin=${f/.ribomarkers.tbl/}
	echo "$bin $num"
done  | column -t > num_genes.txt
