import PySimpleGUI as sg
import speech_recognition as sr
import pyperclip

def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        # recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

r = sr.Recognizer()
mic = sr.Microphone()

choices = sr.Microphone.list_microphone_names()

layout = layout = [[sg.Text('DragonPy v0.01a - Capture Device: ')],    
                 [sg.Listbox(choices, size=(100, len(choices)), key='-INPUTDEVICE-', enable_events=True)],    
                 [sg.Button('Begin Capture')],
                 [sg.InputText(key='-INPUTTEXT-')],
                 [sg.Button('Close')]]     

# Create the window
window = sg.Window("DragonPy v0.01a", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Close" or event == sg.WIN_CLOSED:
        break
    
    if values['-INPUTDEVICE-']:
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if microphone_name == values['-INPUTDEVICE-']:
                mic = sr.Microphone(device_index=i)        
                
    if event == "Begin Capture":
        text_input=recognize_speech_from_mic(r, mic)
                # if there was an error, stop the game
        
        if text_input["error"]:
            window['-INPUTTEXT-'].Update("ERROR: {}".format(text_input["error"]))
        else:    
            pyperclip.copy(format(text_input["transcription"]))
            window['-INPUTTEXT-'].Update("{}".format("Copied to clipboard: "+text_input["transcription"]))

window.close()
