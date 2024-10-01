import os
import azure.cognitiveservices.speech as speechsdk

# Set environment variables for Azure Speech service

os.environ["SPEECH_KEY"] = ""
os.environ["SPEECH_REGION"] = ""

def recognize_from_microphone():
    # Initialize speech configuration
    speech_config = speechsdk.SpeechConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        region=os.environ.get('SPEECH_REGION')
    )
    speech_config.speech_recognition_language = "en-US"

    # Initialize audio configuration to use the default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Perform speech recognition
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized."
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        error_message = "Speech Recognition canceled: {}".format(cancellation_details.reason)
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            error_message += " Error details: {}".format(cancellation_details.error_details)
            error_message += " Did you set the speech resource key and region values?"
        return error_message
