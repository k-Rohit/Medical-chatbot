import azure.cognitiveservices.speech as speechsdk

def synthesize_speech(text):
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = "2931e0f28be245d8b62ee293fb488fa9"
    service_region = "eastus"
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Set the voice for speech synthesis
    speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural"
    
    # Use the default speaker as audio output
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Perform speech synthesis
    result = speech_synthesizer.speak_text_async(text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text: {text}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")
