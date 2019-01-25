import sys
import requests
import xml.etree.ElementTree


if __name__ == "__main__":


    genes = sys.argv[1]

    url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=gene&id={}&rettype=xml'.format(genes)

    data = requests.get(url)

    root = xml.etree.ElementTree.parse(data.text).getroot()

    for info in root.tag('Gene-ref'):

        print(info)
