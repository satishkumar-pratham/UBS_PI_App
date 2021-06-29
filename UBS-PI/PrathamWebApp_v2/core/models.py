from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime


class CANDIDATE(AbstractUser):

	location = models.CharField(max_length = 100, null = True)
	isDeleted = models.BooleanField(default = False, null = False)
	
	def __str__(self):
	
		return "Id : {7} username : {0} first_name : {1}  : last_name : {2} email : {3} password : {4} location : {5} is_deleted : {6}".format(self.username, self.first_name, self.last_name, self.email, self.password, self.location, self.isDeleted, self.id)
		#return "username : {0}".format(self.username)


class INTERVIEW(models.Model):

	candidateId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.DO_NOTHING, null = False, related_name = "Candidate_ID")
	
	dateOfSubmission = models.DateField(null = False, auto_now_add = True)
	timeOfSubmission = models.TimeField(null = False, auto_now_add = True)
	
	languageOfSubmission = models.CharField(max_length = 100, null = True)
	
	isVideo = models.BooleanField(null = True)
	isReportGenerated = models.BooleanField(null = False, default = False)
	isVideoProcessed = models.BooleanField(null = False, default = False)
	isAudioProcessed = models.BooleanField(null = False, default = False)
	isTranscriptProcessed = models.BooleanField(null = False, default = False)
	isTranscriptGenerated = models.BooleanField(null = False, default = False)
	
	videoFilePath = models.TextField(null = True)
	videoFileName = models.TextField(null = True)
	audioFilePath = models.TextField(null = True)
	audioFileName = models.TextField(null = True)
	transcriptFilePath = models.TextField(null = True)
	transcriptFileName = models.TextField(null = True)
	
	eyeContactIndex = models.CharField(null = True, max_length = 50)
	smileIndex = models.CharField(null = True, max_length = 50)
	lipBiteIndex = models.CharField(null = True, max_length = 50)
	faceObstructionIndex = models.CharField(null = True, max_length = 50)
	nlpPositivityIndex = models.CharField(null = True, max_length = 50)
	voiceConfidenceIndex = models.CharField(null = True, max_length = 50)
	
	reportFilePath = models.TextField(null = True)
	reportFileName = models.TextField(null = True)
	
	def __str__(self):
	
		return "Id : {0}\n Candidate : {1}\n dateOfSubmission : {2}\n timeOfSubmission : {3}\n languageOfSubmission : {4}\n isVideo : {5}\n isReportGenerated : {6}\n videoFilePath : {7}\n videoFileName : {8}\n audioFilePath : {9}\n audioFileName : {10}\n transcriptFilePath : {11}\n transcriptFileName : {12}\n eyeContactIndex : {13}\n smileIndex : {14}\n lipBiteIndex : {15}\n faceObstructionIndex : {16}\n nlpPositivityIndex : {17}\n voiceConfidenceIndex : {18}\n reportFilePath : {19}\n reportFileName : {20}\n isVideoProcessed : {21}\n isAudioProcessed : {22}\n isTranscriptProcessed : {23}\n isTranscriptGenerated : {24}\n".format(self.id, self.candidateId, self.dateOfSubmission, self.timeOfSubmission, self.languageOfSubmission, self.isVideo, self.isReportGenerated, self.videoFilePath, self.videoFileName, self.audioFilePath, self.audioFileName, self.transcriptFilePath, self.transcriptFileName, self.eyeContactIndex, self.smileIndex, self.lipBiteIndex, self.faceObstructionIndex, self.nlpPositivityIndex, self.voiceConfidenceIndex, self.reportFilePath, self.reportFileName, self.isVideoProcessed, self.isAudioProcessed, self.isTranscriptProcessed, self.isTranscriptGenerated)
		
		


class THRESHOLD(models.Model):


	dateModified = models.DateField(null = False, auto_now = True)
	
	metricName = models.CharField(null = False, max_length = 100)
	metricThresholdValue = models.FloatField(null = False)
	
	
	def __str__(self):
	
	
		return "Date Modified : {0}\nMetric Name : {1}\nMetric Threshold Value : {2}\n".format(self.dateModified, self.metricName, self.metricThresholdValue)
	
