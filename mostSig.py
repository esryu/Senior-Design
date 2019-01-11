#!/usr/bin/env python

import os,sys
import glob

'''
A Script to Find the Top 100 upregulated and downregulated genes from
Cuffdiff output files
'''

def outputTop(outdir,fileName,up,down,header):

    if not os.path.exists(outdir):

        os.makedirs(outdir)

    upFile = '{}/{}_up.diff'.format(outdir,fileName)
    downFile = '{}/{}_down.diff'.format(outdir,fileName)

    uFile = open(upFile,'w+')

    uFile.write(header)

    for i in range(min(len(up),100)):

        uFile.write('{}\n'.format('\t'.join(up[i])))

    uFile.close()


    dFile = open(downFile,'w+')

    dFile.write(header)

    for j in range(min(len(down),100)):

        dFile.write('{}\n'.format('\t'.join(down[j])))

    dFile.close()


def parseGeneExp(inFile):

    #initialize upregulated and downregulated lists
    up = []
    down = []

    contents = open(inFile,'r').readlines()

    header,contents = contents[0],contents[1:]

    for line in contents:

        fields = line.rstrip().split()

        if fields[-1] == 'yes':

            if fields[9] == '-inf':

                pass

                #print(line.rstrip())

            if float(fields[9]) > 0:

                up.append(fields)

            else:

                down.append(fields)

    s_up = sorted(up,key=(lambda x: abs(float(x[9]))),reverse=True)
    s_down = sorted(down,key=(lambda x: abs(float(x[9]))),reverse=True)


    return header, s_up, s_down

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

        header, up,down = parseGeneExp(file)

        outputTop(outdir,fileName,up,down,header)
