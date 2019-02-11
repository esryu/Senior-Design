import json
import sys
import requests

def geneListConverter(geneList):
    fileToConvert = open(geneList, 'r')
    genes = []
    for line in fileToConvert:
        genes.append(line.strip())

    return genes

def addList(genes):
    ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/addList'
    genes_str = '\n'.join(genes)
    description = "Upregulated genes"

    payload = {
        'list': (None, genes_str),
        'description': (None, description)
    }

    response = requests.post(ENRICHR_URL, files=payload)
    if not response.ok:
        raise Exception('Error analyzing gene list')

    data = json.loads(response.text)
    return data

def viewAddedList(data):
    ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/view?userListId=%s'
    user_list_id = data['userListId']
    response = requests.get(ENRICHR_URL % user_list_id)
    if not response.ok:
        raise Exception('Error getting gene list')

    data = json.loads(response.text)
    print(data)


if __name__ == "__main__":

    genes = sys.argv[1]
    #outdir = sys.argv[2]

    #files = findFiles(inputDir)
    geneList = geneListConverter(genes)
    addedList = addList(geneList)
    viewAddedList(addedList)


    for file in files:

        fileName = getFileName(file)

        header, up,down = parseGeneExp(file)

        outputTop(outdir,fileName,up,down,header)
