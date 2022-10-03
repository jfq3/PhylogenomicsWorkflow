# Steps for making the tree

If you have not already, create the conda environment ribotree using the `ribotree.yml` file in my repository Virtual-Environments.

Clone this repository to a directory on your computer.

```
git clone https://github.com/jfq3/PhylogenomicsWorkflow.git
```

Put genomes of interest in the directory genomes; no other files (except `.git.keep`) shoud be present. If you need examples to run this as a tutorial, copy the genomes from the `Example/Genomes` directory. Then enter:

```
conda activate ribotree
cd genomes
python  ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --performProdigal --outPrefix user .fna
```
Alternatively, you could put faa sequence files for your genomes in the `genomes` directory. In that case you do not need to (re-run) Prodigal, and the command would be:

```
cd genomes
python ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --outPrefix user .faa
```
Combine reference protein sequences and genome protein sequences:

```
while read p; do cat ../phyla_ref/phyla_"$p".faa user_"$p".faa > Dataset1_"$p".faa; done < ../hug_marker_list.txt
```

Align the combined protein sequences:

```
while read p; do muscle -align Dataset1_"$p".faa -output Dataset1_"$p".aln --threads 4; done < ../hug_marker_list.txt
```
Trim the alignments with `trimal`:

```
while read p;do trimal -automated1 -in Dataset1_"$p".aln -out Dataset1_"$p".trimmed.aln; done < ../hug_marker_list.txt
```
This can generate many lines of:

```
Error: the symbol '*' is incorrect
```
This is because the muscle alignments may contain the character "*" which designates a single  fully conserved residue. I think trimal shoudl be able to handle it as such, but currently does not. In any event, the results are still good.

The next step is to concatenate the alignments of the ribosomal protein sequences. This is done with the `concat` function in `BinSanity`. So:


```
concat -f . -e .trimmed.aln --Prefix Dataset1 -o Dataset1.PhylaRibosomal.trimmed.concat.aln -N 4
```

The last step is to generate the tree:

```
FastTree -gamma -lg Dataset1.PhylaRibosomal.trimmed.concat.aln > Dataset1.PhylalsRibosomal.trimmed.concat.newick
conda deactivate
```
