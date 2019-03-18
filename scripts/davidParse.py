#! /usr/bin/env python

import sys
import re

'''
A Parser for the Output of DAVID (run through R DAVIDWEBSERVICE library)
'''

def getGOCategory(catgory):

    level = re.match('GOTERM_(.+)_FAT',catgory)

    return level.groups()[0]

def getGoID(goterm):

    goID,goName = goterm.split('~')

    return goID,goName

def getKegg(kegg):

    id,name = kegg.split(':')

    return id,name


def iterateList(contents):

    clusterIDs = []
    clusters ={}
    header = ''

    i = 0

    while i < len(contents):

        if contents[i] == '':

            i += 1
            continue

        if contents[i].startswith("Annotation"):

            terms = re.match(r'Annotation Cluster (\d+)\s+Enrichment Score: (.+)',contents[i])
            cNum,eScore = terms.groups()

            if cNum not in clusters:

                clusterIDs.append(cNum)

                clusters[cNum] = {'escore':-1,'geneset':set(),
                                'go':{'terms':{},'values':{}},
                                'pathway':{'terms':[],'values':{}}}


            clusters[cNum]['escore']= eScore

            #print(cNum,eScore)

            i += 2

            while contents[i] != '':

                if header == '':

                    header = contents[i-1]

                fields = contents[i].split('\t')

                if float(fields[4]) <= 0.05:

                    if fields[0] != 'KEGG_PATHWAY':

                        category = getGOCategory(fields[0])

                        goID,goName = getGoID(fields[1])

                        if category not in clusters[cNum]['go']['terms']:

                            clusters[cNum]['go']['terms'][category] = []

                        if goID not in clusters[cNum]['go']['terms'][category]:

                            clusters[cNum]['go']['terms'][category].append(goID)

                        clusters[cNum]['geneset'].update(','.split(fields[5]))

                        vals = [fields[0],goName] + fields[2:]
            
                        clusters[cNum]['go']['values'][goID] = vals

                    else:

                        id,name = getKegg(fields[1])

                        if id not in clusters[cNum]['pathway']['terms']:

                            clusters[cNum]['pathway']['terms'].append(id)


                        vals = [name] + fields[2:]
                        clusters[cNum]['pathway']['values'][id] = vals


                i += 1

        i += 1

    return clusterIDs,clusters

def getDavidInfo(infile):

    contents = [x.rstrip() for x in open(infile,'r').readlines()]

    return iterateList(contents)


if __name__ == "__main__":

    infile = sys.argv[1]

    contents = [x.rstrip() for x in open(infile,'r').readlines()]

    iterateList(contents)
