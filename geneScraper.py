from Bio import Entrez, SeqIO
import sys
def geneScraper():
	file = sys.argv[1]
	Entrez.email = "sprinkle2love@gmail.com"
	f = open(file, "r")
	lines = f.readlines()
	result = ""
	for line in lines:
		result = result + (line.split('	')[1]) + ","
	handle = Entrez.efetch(db="Gene",id=result, rettype="gb",retmode="text")
	#handle = Entrez.efetch(db="gene",id="APOC1P1",rettype="gb",retmode="text")
	print handle.read()
	handle.close()
geneScraper()