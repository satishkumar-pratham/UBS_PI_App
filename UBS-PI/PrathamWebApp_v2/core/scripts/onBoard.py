from core.models import CANDIDATE
import pandas as pd

candidateListFilePath = "/home/shriniwas/UBSPratham/PrathamWebApp/media/"
candidateListFileName = "candidateList.csv"


"""
"""
def openFile(candidateListFilePath, candidateListFileName):

	try:
	
		listDf = pd.read_csv(candidateListFilePath + candidateListFileName)
		
	except:
	
		print("Unable to open {0}\n".format(candidateListFilePath + candidateListFileName))
		
		exit(1)
		
	return listDf
	
	
"""
"""
def addToDb(listDf):

	added = 0

	for iterator in range(len(listDf)):
	
		try:
		
			temp_candidate = CANDIDATE(username = listDf['username'][iterator], first_name = listDf['first_name'][iterator], last_name = listDf['last_name'][iterator], password = listDf['password'][iterator], email = listDf['email'][iterator], location = listDf['location'][iterator])
			
			temp_candidate.save()
			
			added += 1
			
		except:
		
			print("Unable to add {0}".format(listDf['username'][iterator]))
	
	
	print("\n================================================\n")
	print("\tSuccessfully On boarded {0} candidates\n".format(added))
	print("================================================\n")

		
def run():

	global candidateListFilePath
	global candidateListFileName
	
	listDf = openFile(candidateListFilePath, candidateListFileName)
	
	addToDb(listDf)
	
	
	

