#! /usr/local/env python

import sys
from davidParse import getDavidInfo as david
from goatools.obo_parser import GODag
from goatools.godag_plot import plot_gos, plot_results, plot_goid2goobj

'''
Script to Create Gene Ontology Charts
'''

def findValue(goIDs,val):

    for id in goIDs:

        print(id,str(val))

        if id == val:

            print(id)

    return

def plotGO(clusterIDs,clusters):

    obodag = GODag("../../obo/go.obo")



    for id in clusterIDs:

        success = False

        goIDs = clusters[id]['go']['terms']

        while not success:

            try:

                plot_gos("../../img/CvF/up/CvF_up_{}.png".format(id), goIDs,obodag)

                success = True

            except KeyError as e:

                value = str(e).replace("'",'')

                goIDs.remove(value)



def getDavid(infile):

    return david(infile)


if __name__ == "__main__":

    infile = sys.argv[1]

    #outdir = sys.argv[2]

    clusterIDs,clusters = getDavid(infile)

    plotGO(clusterIDs,clusters)
