from core.models import INTERVIEW
from core.models import THRESHOLD

import csv
import nltk
import docx
from datetime import date
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet 
import random
from PyDictionary import PyDictionary
import traceback
from django.conf import settings

dbFilePath = settings.MEDIA_ROOT+"/media/NLPFiles/"
dbFileName = "dbFile.csv"


reportFilePath = settings.MEDIA_ROOT+"/media/Reports/"

delimiter = " :: "

stopwordsFilePath =settings.MEDIA_ROOT+ "media/NLPFiles/"
stopwordsFileName = "stopwords.txt"
stopwordsList = []

synnThreshold = 6




"""
input : file path (str), file name (str), mode (str) [default to read mode "r"]
function : open a file in specified mode
output : file object (object of _io.TextIOWrapper)
"""
def openFile(filePath, fileName, mode = "r"):

	fileObj = None

	try:
	
		fileObj = open(filePath + fileName, mode)

	except:
	
		print("\n\n::Unable to open {0}::\n\n".format(fileName))
		
		exit(1)

	return fileObj
	


"""
"""
def generateDataBaseDictionary(dbFileObj):

	global delimiter

	dbDict = dict()
	
	for line in list(dbFileObj):
	
		dbDict[line[0]] = line[1].split(delimiter)
		
	return dbDict


"""
input : stopwords file path (str), stopwords file name(str)
functionality : create stopwords list form given file
output : stop words list (set of str)
"""
def generateStopwordsList(stopwordsFilePath, stopwordsFileName):

	stopwordsList = []

	try:
	
		fileobj = open(stopwordsFilePath + stopwordsFileName,"r")
	
	except:
	
		errorMsg = "Error in openeing file " + stopwordsFileName
		
		print(errorMsg)
		
		exit(1)
		
			
	list_of_lines = fileobj.readlines()
	stopwordsList = set([x.split("\n")[0] for x in list_of_lines])
	
	return stopwordsList


"""
"""
def calculateCount(vector):

	countDict = dict()
	
	for word in vector:
		
			countDict[word] = countDict.get(word, 0) + 1
			
	return countDict
	


"""
"""
def generateTranscriptDictionary(transcript):

	global stopwordsList

	cleanData = transcript.translate(str.maketrans('', '', string.punctuation))
	cleanData = cleanData.replace('\'','')
	cleanData = cleanData.replace(chr(8217),'')
	vector = word_tokenize(cleanData)
	vector = [word.lower() for word in vector]
	vector = [word for word in vector if not word in stopwordsList]
	
	transcriptDict = calculateCount(vector)
	
	return transcriptDict




"""
"""
def generateSynnSet(word):

	"""
	synnSet = set()

	syns = wordnet.synsets(word)
	
	if(len(syns) > 0):
	
		for s in syns:
		
			synnWord = s.lemmas()[0].name()
			
			if(synnWord != word):
			
				synnSet.add(synnWord)
				
	return synnSet
	"""
	
	if(len(word) == 1):
	
		print(ord(word))
	
	englishDictionary = PyDictionary()
	
	synnList = englishDictionary.synonym(word)
	
	return synnList if synnList != None else list()
	


"""
"""
def findSynn(transcriptDict):

	global synnThreshold
	
	text = "It is always beneficial to use rich vocabulary, for some words regularly used by you try to use their synonyms.\n\n"
	
	found = False
	
	for word in transcriptDict.keys():
	
		if(transcriptDict[word] > synnThreshold):
		
			found = True
			
			synnSet = generateSynnSet(word)
			
			if(len(synnSet) > 0):
			
				text += word + " : " + ", ".join(list(synnSet)) + "\n"
			
	return text if found else ""



"""
"""
def generateText(name = "", eyeContactIndex = None, smileIndex = None, nlpPositivityIndex = None, lipBiteIndex = None, faceObstructionIndex = None, voiceConfidenceIndex = None, isVideo = True, transcript = "", dbDict = None):

	transcriptDict = generateTranscriptDictionary(transcript)
	
	text = ""
	
	text += random.choice(dbDict["greeting"]).replace('name', name) + "\n\n"
	text += random.choice(dbDict["open1"]) + " " + random.choice(dbDict["open2"]) + "\n\n"
	
	
	if(eyeContactIndex != None):
			
		text += random.choice(dbDict["eyeContactIndex" + eyeContactIndex]) + "\n\n"
	
	if(smileIndex != None):
	
		text += random.choice(dbDict["smileIndex" + smileIndex]) + "\n\n"
	
	if(lipBiteIndex != None):
	
		text += random.choice(dbDict["lipBiteIndex" + lipBiteIndex]) + "\n\n"
		
	if(faceObstructionIndex != None):
	
		text += random.choice(dbDict["faceObstructionIndex" + faceObstructionIndex]) + "\n\n"	
	
	if(nlpPositivityIndex != None):
			
		text += random.choice(dbDict["sentimentIndex" + nlpPositivityIndex]) + "\n\n"
	
		text += findSynn(transcriptDict)
	
	if(voiceConfidenceIndex != None):
	
		text += random.choice(dbDict["voiceConfidenceIndex" + voiceConfidenceIndex]) + "\n\n"
	
	
	if(isVideo):
	
		if(not eyeContactIndex or not smileIndex or not lipBiteIndex or not faceObstructionIndex):
		
			text += random.choice(dbDict["guidelines"]) + "\n\n"	
	
	text += "\n" + random.choice(dbDict["close1"])
	text += "\n\nThank you & Best Regards\nTeam Pratham"
	
	return text



"""
"""
def writeToFile(reportFilePath, evalText, interview):

	reportFileName = str(interview.id) + "_Report" + ".txt"
	
	fileObj = openFile(reportFilePath, reportFileName, mode = "w")

	try:

		fileObj.write(evalText)
		
		interview.reportFilePath = reportFilePath
		interview.reportFileName = reportFileName
		
		interview.isReportGenerated = True
	
	except:
	
		print(traceback.print_exc())
	
		print("Unable to write to file : {0}".format(reportFilePath + reportFileName))
	
	


"""
"""
def run():

	global stopwordsList

	listOfInterviews = INTERVIEW.objects.filter(isVideoProcessed = True)
	listOfInterviews = listOfInterviews.filter(isAudioProcessed = True)
	listOfInterviews = listOfInterviews.filter(isTranscriptProcessed = True)
	listOfInterviews = listOfInterviews.filter(isReportGenerated = False)
	
	stopwordsList = generateStopwordsList(stopwordsFilePath, stopwordsFileName)

	dbFileObj = csv.reader(openFile(dbFilePath, dbFileName, mode = "r"))
	dbDictVal = generateDataBaseDictionary(dbFileObj)


	for interview in listOfInterviews:

		try:

			textData = open(interview.transcriptFilePath + interview.transcriptFileName).read()

		except:
		
			print("Cannot open Transcript file {0}".format(interview.transcriptFilePath + " " + interview.transcriptFileName))
			

		try:

			nameVal = interview.candidateId.first_name + " " + interview.candidateId.last_name
			
			isVideoVal = interview.isVideo
			
			eyeContactIndexVal = interview.eyeContactIndex
			smileIndexVal = interview.smileIndex
			lipBiteIndexVal = interview.lipBiteIndex
			faceObstructionIndexVal = interview.faceObstructionIndex
			nlpPositivityIndexVal = interview.nlpPositivityIndex
			voiceConfidenceIndexVal = interview.voiceConfidenceIndex

			
			evalText = generateText(name = nameVal, eyeContactIndex = eyeContactIndexVal, smileIndex = smileIndexVal, nlpPositivityIndex = nlpPositivityIndexVal, lipBiteIndex = lipBiteIndexVal, faceObstructionIndex = faceObstructionIndexVal, voiceConfidenceIndex = voiceConfidenceIndexVal, isVideo = isVideoVal, transcript = textData, dbDict = dbDictVal)
			
			writeToFile(reportFilePath, evalText, interview)
			
			interview.save()
		
		except:
		
			print(traceback.print_exc())
		
			print("Cannot Process Interview id {0}".format(interview.id))
		
		
