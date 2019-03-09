#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context

import sys
sys.path.append('../')

import logging
import traceback as tb
import suds.metrics as metrics
from tests import *
from suds import *
from suds.client import Client
from datetime import datetime

errors = 0

setup_logging()

logging.getLogger('suds.client').setLevel(logging.DEBUG)

url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    
print 'url=%s' % url

#
# create a service client using the wsdl.
#
client = Client(url)
client.wsdl.services[0].setlocation('https://david.ncifcrf.gov/webservice/services/DAVIDWebService.DAVIDWebServiceHttpSoap11Endpoint/')
#
# print the service (introspection)
#
#print client

#authenticate user email 
client.service.authenticate('esryu@ucsd.edu')

#add a list 

inputIds = '342,158835,712,101928448,100129385,6358,6348,909,914,963,1469,1576,284233,245937,8447,149647,2205,2214,83888,51738,101926896,2922,2940,57817,51179,3039,3040,3010,8335,3018,121504,27306,91353,3561,3820,353288,8689,81850,337959,100505753,337882,337972,728279,85294,643803,388818,83897,85285,653240,83755,85291,85290,85289,81871,100132476,728224,100132386,83899,83900,85280,81870,353144,100873962,100874253,101929539,101928134,101928135,101929679,101929719,102723649,340357,7940,79136,4161,2315,4332,4496,84560,256236,4759,2831,9970,5126,5341,79057,6039,10647,284402,6343,101928931,153328,6588,57152,26819'

idType = 'ENTREZ_GENE_ID'
listName = 'make_up'
listType = 0
print client.service.addList(inputIds, idType, listName, listType)

#print client.service.getDefaultCategoryNames()
# setCategories
#categorySting = str(client.service.setCategories('BBID,BIOCARTA,COG_ONTOLOGY,GOTERM_BP_FAT,GOTERM_CC_FAT,GOTERM_MF_FAT,INTERPRO,KEGG_PATHWAY,OMIM_DISEASE,PIR_SUPERFAMILY,SMART,SP_PIR_KEYWORDS,UP_SEQ_FEATURE'))


#getChartReport
thd = 0.1
ct = 2
chartReport = client.service.getChartReport(thd,ct)
chartRow = len(chartReport)
print 'Total chart records:',chartRow

#parse and print chartReport
resF = 'list1.chartReport.txt'
with open(resF, 'w') as fOut:
	fOut.write('Category\tTerm\tCount\t%\tPvalue\tGenes\tList Total\tPop Hits\tPop Total\tFold Enrichment\tBonferroni\tBenjamini\tFDR\n')
	for simpleChartRecord in chartReport:
            categoryName = simpleChartRecord.categoryName
            termName = simpleChartRecord.termName
            listHits = simpleChartRecord.listHits
            percent = simpleChartRecord.percent
            ease = simpleChartRecord.ease
            Genes = simpleChartRecord.geneIds
            listTotals = simpleChartRecord.listTotals
            popHits = simpleChartRecord.popHits
            popTotals = simpleChartRecord.popTotals
            foldEnrichment = simpleChartRecord.foldEnrichment
            bonferroni = simpleChartRecord.bonferroni
            benjamini = simpleChartRecord.benjamini
            FDR = simpleChartRecord.afdr
            rowList = [categoryName,termName,str(listHits),str(percent),str(ease),Genes,str(listTotals),str(popHits),str(popTotals),str(foldEnrichment),str(bonferroni),str(benjamini),str(FDR)]
            fOut.write('\t'.join(rowList)+'\n')
   	print 'write file:', resF, 'finished!'
