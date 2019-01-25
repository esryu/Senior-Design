
from Bio import Entrez, SeqIO
import sys
def geneScraper():
	file = sys.argv[1]
	Entrez.email = "sprinkle2love@gmail.com"
	f = open(file, "r")
	lines = f.readlines()
	results = []
	for line in lines:
		gene = line.split('\t')[1]
                if gene not in results:

                    results.append(gene)
        resultString = ','.join(results)
	handle = Entrez.efetch(db="Gene",id=resultString, rettype="gb",retmode="text")
	#handle = Entrez.efetch(db="gene",id="APOC1P1",rettype="gb",retmode="text")
	print handle.read()
	handle.close()
geneScraper()
