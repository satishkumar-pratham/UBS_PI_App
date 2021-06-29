import os

def run():

	print("Starting Video Processing")
	os.system("python3 manage.py runscript videoProcess")
	print("Completed Video Processing")
	
	#print("Starting Audio Processing")
	#os.system("")#TODO RUN AUDIO METRIC CODE
	#print("Completed Audio Processing")
	
	print("Starting Transcript Generation")
	os.system("python3 manage.py runscript generateTranscript")
	print("Completed Transcript Generation")
	
	print("Starting Transcript Processing")
	os.system("python3 manage.py runscript findSentiment")	
	print("Completed Trancript Processing")
	
	print("Starting Report Generation")
	os.system("python3 manage.py runscript generateReport")
	print("Completed Report Generation")
