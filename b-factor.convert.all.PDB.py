#!/usr/bin/env python

# https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
# https://biopython.org/docs/latest/api/Bio.PDB.Chain.html
# pyinstaller --onefile -w ".\b-factor.convert.all.PDB.py"

from Bio.PDB.PDBParser import PDBParser
import tempfile ,os , re, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def extractBFactor(filename) :
    #pdbl = PDBList()
    #pdbl.retrieve_pdb_file("6hyj")

    parser = PDBParser()
    structure = parser.get_structure(filename+".pdb", filename+".pdb")

    resBFactor=[]

    for model in structure:
        for chain in model:
            for residue in chain:
                i=0
                sumBF=0
                if residue.get_resname() != "HOH" :
                    for atom in residue:
                        i+=1
                        sumBF+=atom.get_bfactor()
                    resBFactor+=[[residue.id[1],residue.get_resname(),sumBF/i]]
    #print(resBFactor)

    resBFactorStr=""
    resBFactorPlot=[]

    for i in resBFactor:
        resBFactorStr+=f'{i[0]}\t{i[1]}\t{round(i[2],3)}\n'
        resBFactorPlot+=[[i[0],i[1]]]

    fo = open(filename+".resbfactors.txt", "w+")
    fo.write(resBFactorStr)
    fo.close()
    #fig, ax = plt.subplots()
    df=pd.DataFrame(data=resBFactor, index=None, columns=["Residue","Name","B-Factor"])
    sns.relplot(x="Residue", y="B-Factor", kind="line", data=df)
    plt.savefig(filename+'.resbfactors.png')
    return True


for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if(file.endswith(".pdb")):
            #print(os.path.join(root,file))
            extractBFactor(os.path.splitext(file)[0])