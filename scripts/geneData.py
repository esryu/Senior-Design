import sys
import requests
import xml.etree.ElementTree


if __name__ == "__main__":


    genes = sys.argv[1]

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id={}&rettype=xml'.format(genes)

    data = requests.get(url)

    tree = xml.etree.ElementTree.fromstring(data.content)

    print(tree.find('./Entrezgene/Entrezgene_gene/Gene-ref_locus').text)

    #for element in tree.findall('./*/*'):

        #print(element.tag)

    #for element in tree.iter():

        #if element.tag == 'Gene-ref_locus':

            #print(element.__dict__.keys())
            #print(element.text)

    #for info in root.tag('Gene-ref'):

        #print(info)
