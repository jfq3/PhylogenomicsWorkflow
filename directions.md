# Steps for making the tree

If you have not already, create the environment ribotree using the `ribotree.yml` file in my repository Virtual-Environments. I suggest that you use micromamba for creating your environments.  

Clone this repository to a directory on your computer.

```
git clone https://github.com/jfq3/PhylogenomicsWorkflow.git
```

Put genomes of interest in the directory genomes; no other files (except `.git.keep`) shoud be present. If you need examples to run this as a tutorial, copy the genomes from the `Example/Genomes` directory. To so so, cd into the `PhylogenomicsWorkflow/genomes` directory enter:

```
cp ../Example/Genomes/*.fna ./
```
Then enter:

```
micromamba activate ribotree

cd PhylogenomicsWorkflow/genomes # if not already there

python  ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --performProdigal --outPrefix user .fna
```
Alternatively, you could put faa sequence files for your genomes in the `genomes` directory. In that case you do not need to run Prodigal, and the command would be:

```
python ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --outPrefix user .faa
```
The above commands extract the marker genes from the genomes in the `genomes` directory. It can take a few minutes, depending on the number of genomes submitted. When it finishes, it will print to the screen "Made markers list" 16 times, one line for each of the marker genes.  

Combine reference protein sequences and genome protein sequences. In this tutorial, the reference protein sequences are the ones in the `phyla_ref` directory.  

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
This is because the muscle alignments may contain the character "*" which designates a single  fully conserved residue. I think trimal shoudl be able to handle it as such, but currently does not. In any event, you may ignore the error messages. The results are still good.

The next step is to concatenate the alignments of the ribosomal protein sequences. This is done with the `concat` function in `BinSanity`. So:

```
concat -f . -e .trimmed.aln --Prefix Dataset1 -o Dataset1.PhylaRibosomal.trimmed.concat.aln -N 4
```

The last step is to generate the tree:

```
FastTree -gamma -lg Dataset1.PhylaRibosomal.trimmed.concat.aln > Dataset1.PhylaRibosomal.trimmed.concat.newick

micromamba deactivate
```
