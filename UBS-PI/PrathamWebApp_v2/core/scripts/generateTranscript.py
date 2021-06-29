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

import azure.cognitiveservices.speech as speechsdk
import time
import datetime
import os
import moviepy.editor as mp
import glob
import pandas as pd
import traceback


audioFilePath = "media/audios/"
transcriptFilePath = "media/transcripts/"


def Video_To_Audio(interview):

    global audioFilePath

    videoFilePath = interview.videoFilePath
    videoFileName = interview.videoFileName

    not_completed = []

    # if the file has video, it gets converted to audio only
    clip = mp.VideoFileClip(videoFilePath + videoFileName)

    audioFileName = str(interview.id) + "_audio.wav"

    clip.audio.write_audiofile(os.path.join(audioFilePath + audioFileName),
                           codec='pcm_s16le', verbose=False)

    interview.audioFilePath = audioFilePath
    interview.audioFileName = audioFileName

    interview.save()





def convert_audio_to_wav(interview):

    audioFilePath = interview.audioFilePath
    audioFileName = interview.audioFileName

    try:
                    # if the file had no video, it is checked if it has audio and extracts audio
        clip = mp.AudioFileClip(audioFilePath + audioFileName)
        
        audioFileName = str(interview.id) + "_audio.wav"
        
        clip.write_audiofile(os.path.join(audioFilePath + audioFileName),
                             codec='pcm_s16le', verbose=False)
        interview.audioFilePath = audioFilePath
        
        interview.audioFileName = audioFileName
        interview.save()

    except:
    # save the names of files that cannot be converted
        print("File not converted to audio...", audioFileName)
        print(traceback.print_exc())


def speech_to_text(f):

    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    speech_key, service_region = "2a9ce48acf3b4e31bd16ad0dadbe287b", "centralindia"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates an audio configuration that points to an audio file.
    # Replace with your own audio filename.
    audio_filename = f
    audio_input = speechsdk.audio.AudioConfig(filename=audio_filename)
    # Creates a recognizer with the given settings
    speech_config.speech_recognition_language="en-IN"
    #speech_config.request_word_level_timestamps()
    #speech_config.enable_dictation()
    speech_config.output_format = speechsdk.OutputFormat(1)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    #result = speech_recognizer.recognize_once()
    all_results = []



    #https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.recognitionresult?view=azure-python
    def handle_final_result(evt):
        all_results.append(evt.result.text)


    done = False

    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done= True

    #Appends the recognized text to the all_results variable.
    speech_recognizer.recognized.connect(handle_final_result)

    #Connect callbacks to the events fired by the speech recognizer & displays the info/status
    #Ref:https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.eventsignal?view=azure-python
    speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(lambda evt: print('RECOGNIZED: {}'.format(evt)))
    speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()

    while not done:
        time.sleep(.5)

    #print("Printing all results:")
    #print(all_results)
    return all_results




def run():

    global transcriptFilePath

    listOfInterviews = INTERVIEW.objects.filter(isTranscriptGenerated = False)

    for interview in listOfInterviews:

        try:

            if(interview.isVideo == True):

                Video_To_Audio(interview)

            audioFileName = interview.audioFileName

            if(not ('wav' in audioFileName)):

                convert_audio_to_wav(interview)

            #IMP to have interview.audioFileName as it may be changed in convert_audio_to_wav function rather than using the var audioFileName directly
            result = speech_to_text(interview.audioFilePath + interview.audioFileName)

            string=""

            for i in result:

                string = string + i


            transcriptFileName = str(interview.id) + "_transcript.txt"

            try:

                fileObj = open(transcriptFilePath + transcriptFileName, "w")

                fileObj.write(string)

                fileObj.close()

            except:

                print("Unable to open {0}".format(transcriptFilePath + transcriptFileName))
                print(traceback.print_exc())


            interview.transcriptFilePath = transcriptFilePath
            interview.transcriptFileName = transcriptFileName

            interview.isTranscriptGenerated = True

            interview.save()

        except:

            print("Clould not generate transcript for {0}".format(interview.id))
            print(traceback.print_exc())
            
            
