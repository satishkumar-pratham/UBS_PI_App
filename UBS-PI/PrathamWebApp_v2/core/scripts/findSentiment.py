from core.models import INTERVIEW
from core.models import THRESHOLD

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import csv
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

import traceback
from django.conf import settings


stopwordsFilePath = settings.MEDIA_ROOT+"/media/NLPFiles/"
stopwordsFileName = "stopwords.txt"






"""
input : stopwords file path (str), stopwords file name(str)
functionality : create stopwords list form given file
output : stop words list (list of str)
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
	stopwordsList = [x.split("\n")[0] for x in list_of_lines]
	
	return stopwordsList



"""
input : list of transcripts (list of objects of Trascript Class)

output : None

functionality : Performs following for input and database questions -
1) Removes Punctuation marks
2) converts data in lower case
3) Creates Tokens
4) Removes stop words
5) Performs Stemming 
6) Creates vector of words
"""
def cleandata(data, stopwordsList):

	ps = PorterStemmer()

	cleanData = data.translate(str.maketrans('', '', string.punctuation))
	cleanData = cleanData.replace('\'','')
		
	vector = word_tokenize(cleanData)
	vector = [word.lower() for word in vector]
	vector = [word for word in vector if not word in stopwordsList]
	vector = [ps.stem(word) for word in vector]
	
	return vector 



"""
input : list of transcripts (list of objects of Trascript Class)
function : determine sentiment for text
output : None
"""
def findSentiment(vector):

	sid = SentimentIntensityAnalyzer()

	tempDict = sid.polarity_scores(" ".join(vector))
		
	return tempDict["pos"]
		


def run():

	listOfInterviews = INTERVIEW.objects.filter(isTranscriptGenerated = True)
	listOfInterviews = listOfInterviews.filter(isTranscriptProcessed = False)
	
	metric = THRESHOLD.objects.filter(metricName = "sentimentLow")[0]
	t1 = metric.metricThresholdValue
	
	metric = THRESHOLD.objects.filter(metricName = "sentimentMedium")[0]
	t2 = metric.metricThresholdValue

	for interview in listOfInterviews:

		computedIndex = None

		try:

			textData = open(interview.transcriptFilePath + interview.transcriptFileName).read()

		except:
		
			print("Cannot open Transcript file {0}".format(interview.transcriptFilePath + " " + interview.transcriptFileName))

		
		try:
		
			stopwordsList = generateStopwordsList(stopwordsFilePath, stopwordsFileName)

			vector = cleandata(textData, stopwordsList)

			sentimentScore = findSentiment(vector)
		
			if(sentimentScore <= t1):
				computedIndex = 'Low'
			
			elif(sentimentScore <= t2):
				computedIndex = 'Medium'
				
			else:
				computedIndex = 'High'
			
		except(Exception):
		
			print("Error in computing sentiment")
			print(traceback.print_exc())		
			
		finally:
		
			interview.isTranscriptProcessed = True
			
			interview.nlpPositivityIndex = computedIndex;print("here")
		
			interview.save()
			
			
			
			
