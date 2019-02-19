#!/usr/bin/env python

import os,sys
import glob
from geneData import *

'''
A Script to Find the Top 100 upregulated and downregulated genes from
Cuffdiff output files
'''

def outputTop(outdir,fileName,up,down,header,data):

    if not os.path.exists(outdir):

        os.makedirs(outdir)

    upFile = '{}/{}_up.diff'.format(outdir,fileName)
    downFile = '{}/{}_down.diff'.format(outdir,fileName)

    uFile = open(upFile,'w+')

    header = header.rstrip() + '\tDescription\tSummary\n'

    uFile.write(header)

    for i in range(min(len(up),100)):

        name = up[i][0]

        desc = data[name][0]

        summ = data[name][1]

        uFile.write('{}\t{}\t{}\n'.format('\t'.join(up[i]),desc,summ))

    uFile.close()


    dFile = open(downFile,'w+')

    dFile.write(header)

    for j in range(min(len(down),100)):

        dFile.write('{}\n'.format('\t'.join(down[j])))

    dFile.close()

def splitGeneList(genes):

    for subList in [genes[x:x+100] for x in range(0, len(genes), 100)]:

        yield subList


def getGeneData(genes):

    geneDataDict = {}

    for geneList in splitGeneList(genes):

        data = geneData(','.join(geneList))

        geneDataDict.update(data)

    return geneDataDict

def parseGeneExp(inFile):

    #initialize upregulated and downregulated lists
    up = []
    down = []


    #Open and read the contents of the file
    contents = open(inFile,'r').readlines()

    header,contents = contents[0],contents[1:]

    for line in contents:

        fields = line.rstrip().split()

        if fields[-1] == 'yes':


            if float(fields[9]) > 0:

                up.append(fields)

            else:

                down.append(fields)

    s_up = sorted(up,key=(lambda x: abs(float(x[9]))),reverse=True)
    s_down = sorted(down,key=(lambda x: abs(float(x[9]))),reverse=True)

    s_up_100 = s_up[0:100]
    s_down_100 = s_down[0:100]

    genes = set()

    genes.update([x[0] for x in s_up_100])
    genes.update([x[0] for x in s_down_100])

    print(genes)

    return header, s_up_100, s_down_100,list(genes)

def getFileName(file):

    name = os.path.basename(file).split('.')

    nameFields = name[0:len(name)-1]

    return '.'.join(nameFields)



def findFiles(inputDir):

    files = glob.glob('{}/*.diff'.format(inputDir))

    return files

if __name__ == "__main__":


    inputDir = sys.argv[1]
    outdir = sys.argv[2]

    files = findFiles(inputDir)


    for file in files:

        fileName = getFileName(file)

        header,up,down,genes = parseGeneExp(file)

        data = getGeneData(genes)

        outputTop(outdir,fileName,up,down,header,data)
