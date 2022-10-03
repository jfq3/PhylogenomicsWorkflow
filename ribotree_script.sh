#!/bin/bash

# This script is run from the genomes directory

# Extract ribosomal protein sequences form the genomes.
python  ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --performProdigal --outPrefix user .fna

# Combine reference and genome protein sequences

```
while read p; do cat ../phyla_ref/phyla_"$p".faa user_"$p".faa > Dataset1_"$p".faa; done < ../hug_marker_list.txt
```

# Align the combined protein sequences

```
while read p; do muscle -align Dataset1_"$p".faa -output Dataset1_"$p".aln --threads 4; done < ../hug_marker_list.txt
```

# Trim the alignments

```
while read p;do trimal -automated1 -in Dataset1_"$p".aln -out Dataset1_"$p".trimmed.aln; done < ../hug_marker_list.txt
```

# Concatenate the alignments

```
concat -f . -e .trimmed.aln --Prefix Dataset1 -o Dataset1.PhylaRibosomal.trimmed.concat.aln -N 4
```

# Make the tree

```
FastTree -gamma -lg Dataset1.PhylaRibosomal.trimmed.concat.aln > Dataset1.PhylalsRibosomal.trimmed.concat.newick
```



