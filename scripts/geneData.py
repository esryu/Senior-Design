import sys
import requests
import xml.etree.ElementTree

'''
A set of functions to query gene information from NCBI.
'''


def sendRequests(genes):

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id={}&rettype=xml'.format(genes)

    print(url)

    data = requests.get(url)

    tree = xml.etree.ElementTree.fromstring(data.content)

    return tree

def iterateTree(tree):

    for gene in tree.findall('Entrezgene'):

        name = getGeneName(gene)
        desc = getGeneDesc(gene)
        summ = getGeneSummary(gene)

        yield name,desc,summ

#Get the Attributes of Each Gene

def getGeneName(gene):

    return gene.find('Entrezgene_gene/Gene-ref/Gene-ref_locus').text


def getGeneDesc(gene):

    return gene.find('Entrezgene_gene/Gene-ref/Gene-ref_desc').text

def getGeneSummary(gene):

    try:

        return gene.find('Entrezgene_summary').text

    except:

        return 'None'

#Build a Dictionary of gene entries
def geneData(genes):

    tree = sendRequests(genes)

    geneData = {}

    for name,desc,summ in iterateTree(tree):

        geneData[name] = [desc,summ]

    return geneData

if __name__ == "__main__":


    genes = sys.argv[1]

    tree = sendRequests(genes)

    iterateTree(tree)

