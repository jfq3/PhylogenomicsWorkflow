# Steps for making the tree

If you have not already, create the environment ribotree using the `ribotree.yml` file in my repository Virtual-Environments. I suggest that you use micromamba for creating your environments.  

**1. Clone this repository to a directory on your computer.**

```
git clone https://github.com/jfq3/PhylogenomicsWorkflow.git
```
**2. Submit genomes to be treed**  

Put genomes of interest in the directory genomes; no other files (except `.git.keep`) shoud be present. If you need examples to run this as a tutorial, copy the genomes from the `Example/Genomes` directory. To do so, cd into the `PhylogenomicsWorkflow/genomes` directory and enter:

```
cp ../Example/Genomes/*.fna ./
```
**3. Search genomes for marker genes**

Enter:

```
micromamba activate ribotree

cd PhylogenomicsWorkflow/genomes # if not already there

python  ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --performProdigal --outPrefix user .fna
```
Alternatively, you could put `faa` sequence files for your genomes in the `genomes` directory. In that case you do not need to run Prodigal, and the command would be:

```
python ../identifyHMM.py --markerdb ../hug_ribosomalmarkers.hmm --outPrefix user .faa
```
The above commands extract the marker genes from the genomes in the `genomes` directory. It can take a few minutes, depending on the number of genomes submitted. When it finishes, it will print to the screen "Made markers list" 16 times, one line for each of the marker genes.  

**Optional - Count marker genes found**

When treeing your own genomes, it is a good idea to count the number of reference genes found in each. If too few are found in a genome, it will affect the branch length and possibly the placement of that genome in the tree. "Too few" is a judgment call - it largely depends on how genomes with fewer marker genes appear in the tree. As a general rule, I am suspicious if fewer than 75% of the reference genes are found. If you notice an association between the number of marker genes found and the placement of the genomes in the tree, you might decide to remove the genome(s) with fewer marker genes and re-run the tree building.  

While in the `genome` directory, enter:  

```
cp ../count_genes.sh ./
chmod u+x count_genes.sh
./count_genes.sh
less num_genes.txt
```
The script deletes any pre-existing `num_genes.txt` file and creates one consisting of two columns: the name of the genome and the number of marker genes found. For this marker gene set, the maximum is 16.  

**4. Combine reference and submitted marker gene sequences**  

Combine reference protein sequences and genome protein sequences. In this tutorial, the reference protein sequences are the ones in the `phyla_ref` directory. Edit the path to the reference protein sequences as necessary for your use case.   

```
while read p; do cat ../phyla_ref/phyla_"$p".faa user_"$p".faa > Dataset1_"$p".faa; done < ../hug_marker_list.txt
```

**5. Align the combined protein sequences:**

Enter:
```
while read p; do muscle -align Dataset1_"$p".faa -output Dataset1_"$p".aln --threads 4; done < ../hug_marker_list.txt
```
**6. Trim the alignments with `trimal`**

Enter:
```
while read p;do trimal -automated1 -in Dataset1_"$p".aln -out Dataset1_"$p".trimmed.aln; done < ../hug_marker_list.txt
```
This can generate many lines of:

```
Error: the symbol '*' is incorrect
```
This is because the muscle alignments may contain the character "*" which designates a single  fully conserved residue. I think trimal shoudl be able to handle it as such, but currently does not. In any event, you may ignore the error messages. The results are still good.

**7. Concatenate the alighments**  

The next step is to concatenate the alignments of the ribosomal protein sequences. This is done with the `concat` function in `BinSanity`, so:

```
concat -f . -e .trimmed.aln --Prefix Dataset1 -o Dataset1.PhylaRibosomal.trimmed.concat.aln -N 4
```

**8. Generate the tree***  

The last step is to generate the tree with FastTree:

```
FastTree -gamma -lg Dataset1.PhylaRibosomal.trimmed.concat.aln > Dataset1.PhylaRibosomal.trimmed.concat.newick

micromamba deactivate
```
Visualize the tree (file Dataset1.PhylaRibosomal.trimmed.concat.newick) by loading it into a tree viewer, *e.g.* FigTree.  