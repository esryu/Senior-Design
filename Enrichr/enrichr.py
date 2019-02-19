import json
import sys
import requests

def geneListConverter(geneList):
    fileToConvert = open(geneList, 'r')
    genes = []
    for line in fileToConvert:
        genes.append(line.strip())

    return genes

def libraryListConverter(libraryList):
    fileToConvert = open(libraryList, 'r')
    libraries = []
    for line in fileToConvert:
        libraries.append(line.strip())

    return libraries


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

def enrich(data, libraries, txtfile):
    ENRICHR_URL = 'http://amp.pharm.mssm.edu/Enrichr/enrich'
    query_string = '?userListId=%s&backgroundType=%s'
    user_list_id = data['userListId']
    #gene_set_library = 'KEGG_2015'
    writtenFile = open(txtfile, 'w')
    libraryScores = []

    libraryData = {}

    libraryScores = []
    for library in libraries:
        response = requests.get(
            ENRICHR_URL + query_string % (user_list_id, library)
            )
        data = json.loads(response.text)
        for key, values in data.items():

            combinedScore = -1

            try:

                combinedScore = values[0][4]
            except IndexError:

                print(key,values)
                
            libraryData[key] = values
            tupleScore = (key, combinedScore)
            print(tupleScore)
            libraryScores.append(tupleScore)


        #print(libraryData)
        #print(libraryData)
        #print("Done with " + library + '\n\n')
    sortedLibraries = sorted(libraryScores,key=lambda x: x[1],reverse=True)
    print(sortedLibraries)
    sortedFile = open('sortedLibraries.txt','w+')
    sortedFile.write('{}\t{}\n'.format(x[0],str(x[1])) for x in sortedLibraries)
    writtenFile.write(str(data) + "\n")
    if not response.ok:
        raise Exception('Error fetching enrichment results')


    writtenFile.close()

    return libraryData

def pullCombinedScore(term):
    return term[0][4]

def sortCombinedScores(enrichrData):
    newSortedList = []
    enrichrData.sort(key=pullCombinedScore)
    return 0



if __name__ == "__main__":

    genes = sys.argv[1]
    libraries = sys.argv[2]
    nameOfLibraryDataFile = sys.argv[3]


    #files = findFiles(inputDir)
    geneList = geneListConverter(genes)
    libraryList = libraryListConverter(libraries)
    addedList = addList(geneList)
    viewAddedList(addedList)
    fileToSort = enrich(addedList, libraryList, nameOfLibraryDataFile)


    '''
    for file in files:

        fileName = getFileName(file)

        header, up,down = parseGeneExp(file)

        outputTop(outdir,fileName,up,down,header)
    '''
