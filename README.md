# README

The objective of this workflow is to place genomes of interest in a tree of reference genomes using concatenated alignments of 16 ribosomal proteins that tend to be syntenic and colocated. These 16 ribosomal proteins were used in [Hug et al. 2016](https://doi.org/10.1111/1462-2920.12930).

I had several problems following the original tutorial hosted at https://github.com/edgraham/PhylogenomicsWorkflow.

For one, the indentation in the python script identifyHMM was not consistent. In this repository, I have renamed the script by adding the extention ".py" and made the indentation consistent.

Another problem I had was installing the requirements in a single conda environment. The original README.md gives instrucitons  for a native installation and specifies python 2.7, but BinSanity is a python 3 script. I think this is the reason conda was never able to solve a single environment.  I solved the problem by converting identifyHMM.py from a python 2.7 script to python 3 and not specifying a python version when creating the environment. 

I also had to edit the MUSCLE command to work with the newer version of MUSCLE that is part of the `ribotree` environment I created.  

I suggest that you use `micromamba` to manage your conda environments. If you are using `conda` or `mamaba`, substitute one of those names in the installation code below:    

```
cd
wget https://github.com/jfq3/Virtual-Environments/raw/master/ribotree.yml
micromamba env create -f ribotree.yml
```

Instructions for this workflow are in the file `directions.md`.  

There are three reference data sets in this repository.  

**`phyla_lite`**  
 To place unknown genomes in relation to known phyla, I made a reference set from the genomes in the MiGA Phyla\_Lite database. There is one genome per phylum.  I made this database by running identifyHMM on the Phyla\_Lite genomes. 
 
**`phyla_ref_edited`**
This is the same data base as `phyla_lite` except that I shortened the names to just genus and species by removing the genome identifier.  

**`HugRef`**
The reference data from the original repository. It was made from 100 *Pseudomonadota* genomes belonging to the *Alpahproteobacteria* and *Gammaproteobacteria*. It is under the `Example` directory.  

## Read the `directions.md` file for how to create a tree following my changes. ##

The following was extracted from the README file for the original repository.  

The script relies on the user providing the location of a file containing Hidden Markov Models (HMMs) for their genes of interest. Here we have provided you with a file called `hug_ribosomalmarkers.hmm`. This contains HMM models for 16 Ribosomal proteins: RpL14, RpL15, RpL16 ,RpL18, RpL22, RpL24 ,RpL2, RpL3, RpL4, RpL5, RpL6, RpS10, RpS17, RpS19, RpS3, RpS8. 

The help message for `identifyHMM` is given below:

```
usage: identifyHMM [-h] [--markerdb MARKERDB] [--performProdigal] [--cut_tc]
                   [--outPrefix OUTPREFIX] [--Num NUM] [-E E]
                   Input

Identify marker genes in in protein sequences of genomes.

positional arguments:
  Input                 Target file(s). Provide unifying text of desired
                        genome(s). Ext must be 'fna' or 'faa'.

optional arguments:
  -h, --help            show this help message and exit
  --markerdb MARKERDB   Provide HMM file of markers. Markers should have a
                        descriptive ID name.
  --performProdigal     Run Prodigal on input genome nucleotide FASTA file
  --cut_tc              use hmm profiles TC trusted cutoffs to set all
                        thresholding
  --outPrefix OUTPREFIX
                        Provide prefix of names for marker output files.
  -E E                  Set E-Value to be used in hmmsearch. Default: 1E-5

```
