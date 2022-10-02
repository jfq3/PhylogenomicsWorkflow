# Steps for making the tree

Put genomes of interest in the directory genomes; no other files shoud be present. If you need examples, copy the genomes form the `Example/Genomes` folder. Then enter:

```
cd /genomes
python  ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --performProdigal --outPrefix user .fna
```
Alternatively, you could put * files in genomes, In that case you do not need to (re-run) Prodigal, and the command would be:


```
cd genomes
../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --outPrefix phyla .faa
```
Combine reference protein sequences and genome protein sequences

```
while read p; do cat ../phyla_ref/phyla_"$p".faa user_"$p".faa > Dataset1_"$p".faa; done < ../hug_marker_list.txt
```
Align the combined protein sequences:

```
while read p; do muscle -align Dataset1_"$p".faa -output Dataset1_"$p".aln; done < ../hug_marker_list.txt
```
Trim the laignments with trimal:

```
while read p;do trimal -automated1 -in Dataset1_"$p".aln -out Dataset1_"$p".trimmed.aln; done < ../hug_marker_list.txt
```
This can generates many lines of:

```
Error: the symbol '*' is incorrect
```
This is because the muscle alignments may contain the character "*" which designates a single  fully conserved residue. I think trimal shludl be able to handle it as such. Maybe an aligner other than muscle would be better? But other alignments also generate the same.

The next step is to concatenate the alignments of the ribosomal protein sequences. This is done with the 'concat' function in 'BinSanity' which I had to create in a separate conda environment. So:


```
conda deactivate
conda activate binsanity

concat -f . -e .trimmed.aln --Prefix Dataset1 -o Dataset1.PhylaRibosomal.trimmed.concat.aln -N 4

conda deactivate
conda activate ribotree
```

The last sep is to generate the tree:

```
FastTree -gamma -lg Dataset1.PhylaRibosomal.trimmed.concat.aln > Dataset1.PhylalsRibosomal.trimmed.concat.newick
```



