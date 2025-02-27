#!/usr/bin/python

"""
Using a set of phylogenetic markers BLAST protein sequences of target
organisms to identify markers.

Determine number of markers present in target.

Output FASTA only if more than half of targets are present
"""

import sys
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast import NCBIXML
import os,shutil
import glob
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import argparse
import subprocess
parser = argparse.ArgumentParser(description="Identify marker genes in\
                                in protein sequences of genomes.")
parser.add_argument('Input', help="Target file(s). Provide unifying \
                    text of desired genome(s). Ext must be 'fna' or 'faa'.")
parser.add_argument('--markerdb', help='Provide HMM file of markers. \
                    Markers should have a descriptive ID name.')
parser.add_argument('--performProdigal', action='store_true', help='Run \
                    Prodigal on input genome nucleotide FASTA file')
parser.add_argument('--cut_tc',action='store_true',help="use hmm profiles TC trusted cutoffs to set all thresholding")
parser.add_argument('--outPrefix', help='Provide prefix of names for marker \
                    output files.')
parser.add_argument('-E',help='Set E-Value to be used in hmmsearch. Default: 1E-5',default='1E-5')
args = parser.parse_args()
arg_dict = vars(args)
Evalue = arg_dict['E']
outname = arg_dict['outPrefix']
if arg_dict["performProdigal"] == True:
    input_fasta = glob.glob("*%s" % (arg_dict['Input']))
    for in_fna in input_fasta:
        name = in_fna.rsplit('.',1)[0]
        subprocess.call(["prodigal","-a", "temp1.orfs.faa", "-i",in_fna,"-m","-o", "temp1.txt","-p","meta","-q"])
        outfile=open(str((name)+".faa"),"w")
        subprocess.call(["cut","-f1","-d"," ","temp1.orfs.faa"],stdout=outfile)
        os.remove("temp1.orfs.faa")
        os.remove("temp1.txt")

input_proteins = glob.glob("*.faa")

markerdb = arg_dict['markerdb']
marker_list = []
for line in open(markerdb, "r"):
    line = line.rstrip()
    if line[:4] == "NAME":
        marker_list.append(line.split()[1])
        print("Made markers list")
num_markers = len(marker_list)

for in_faa in input_proteins:
    name_protein = in_faa.rsplit('.',1)[0]
    hmmer_log = open("hmmsearhc-log.txt","w")
    if arg_dict["cut_tc"] == "True":
        subprocess.call(["hmmsearch","--cut_tc","--tblout",str(str(name_protein)+".ribomarkers.tbl"),"--notextw",markerdb, str(in_faa)],stdout=hmmer_log)
    else:
        subprocess.call(["hmmsearch","-E",Evalue,"--tblout",str(str(name_protein)+".ribomarkers.tbl"),"--notextw",markerdb, str(in_faa)],stdout=hmmer_log)
genome_marker_count = {}
hmm_names = glob.glob("*ribomarkers.tbl")
for active_hmm in hmm_names:    
    genome_name = active_hmm[:-16]
    if os.stat(active_hmm).st_size < 1000:
        genome_marker_count[genome_name] = {}
    for line in open(str(active_hmm), "r"):
        line = line.rstrip()
        if line[0] != "#":
            line_info = line.split()
            try:
                if line_info[2] in list(genome_marker_count[genome_name].keys()):
                    if line_info[0] != genome_marker_count[genome_name][line_info[2]]:
                        genome_marker_count[genome_name][line_info[2]] = "empty"
                else:
                    genome_marker_count[genome_name][line_info[2]] = line_info[0]
            except KeyError:
                genome_marker_count[genome_name] = {}
                genome_marker_count[genome_name][line_info[2]] = line_info[0]


for genome in genome_marker_count:
    remove = []
    for i in genome_marker_count[genome]:
        if genome_marker_count[genome][i] == "empty":
            remove.append(i)
    for x in remove:
        del genome_marker_count[genome][x]
    if float(len(list(genome_marker_count[genome].keys()))) >= 1:
        reverse_gene_info = {}
        for k in genome_marker_count[genome]:
            reverse_gene_info[genome_marker_count[genome][k]] = k
    for record in SeqIO.parse(open(str(str(genome)+".faa"), "r"), "fasta"):
        if record.id in list(reverse_gene_info.keys()):
            marker = reverse_gene_info[record.id]
            out_file = open("%s_%s.faa" % (outname, marker), "a")
            out_file.write(">%s\n" % (genome) +str(record.seq)+"\n")
            out_file.close()
    if float(len(list(genome_marker_count[genome].keys()))) < float(1):
        print(str(genome) + " markers = " + str(len(list(genome_marker_count[genome].keys()))))

