"""

This file is created as template for all driver codes, this will cater to transcript generation, processing, audio processing, video processing and report generation.

The basic structure is as follows : 

1) read rows from database where respective flag is not set (for example for sentiment : where isTranscriptProcessed = False should be retrieved)
2) iterate over each row and perform required operation
3) for each row set the flag to true EVEN IF ERROR OCCURS
4) Save the modified row so that updates are made in the database
5) Generate logs of error if required
6) this complete code must be part of a 'run' function
7) Also Use the THRESHOLD table to identify required value


"""

from core.models import INTERVIEW
from core.models import THRESHOLD

def run():

	listOfInterviews = INTERVIEW.objects.filter(isTranscriptProcessed = False) #TODO use required flag

	#metric = THRESHOLD.objects.filter(metricName)[0]
	#t1 = metric.metricThresholdValue

	for interview in listOfInterviews:

		#file = open(interview.path + interview.fileName)

		#score = someMetric(file)

		#if(score > t1):
			#interview.sentimentIndex = 'High'
		
		#interview.isTranscriptProcessed = True #TODO use required flag
		
		interview.save()
