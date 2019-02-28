import mygene
import sys

mg = mygene.MyGeneInfo()

def retrieveGenes(genes):
    officialGeneList = open(genes, 'r')

    geneList = []
    for line in officialGeneList:
        geneList.append(line.strip())

    return geneList

def convertGenes(geneList):
    #entrezDict = []
    #for gene in geneList:
    entrezDict = mg.querymany(geneList, scopes='symbol', fields='entrezgene', species='human')
    #entrezDict.append(out)

    return entrezDict

def dictToList(entrezDict):
    finalList = []
    for entrezGene in entrezDict:

        entrezID = ''
        try:
            entrezID = entrezGene['entrezgene']
        except:

            entrezID = 'None'

        finalList.append(entrezID)
    #    for key,value in entrezGene.items():
    #        finalList.append(value)

    return finalList

def moveToFile(finalList, entrezFile):
    finalTxtFile = open(entrezFile, 'w')
    for ID in finalList:
        if ID != 'None':
            finalTxtFile.write(ID)
            finalTxtFile.write('\n')

if __name__ == "__main__":

    genes = sys.argv[1]
    nameOfEntrezFile = sys.argv[2]
    geneList = retrieveGenes(genes)
    print(geneList)
    entrezDict = convertGenes(geneList)
    print(entrezDict)
    finalList = dictToList(entrezDict)
    print(finalList)
    moveToFile(finalList, nameOfEntrezFile)
