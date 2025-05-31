# transcribe_google.py
import speech_recognition as sr

r = sr.Recognizer()

# Use default or choose "Stereo Mix" if needed
with sr.Microphone(device_index=None) as source:
    print("Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=2)
    print("Listening...")

    try:
        while True:
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                print("You said:", text)
            except sr.UnknownValueError:
                print("Google could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

    except KeyboardInterrupt:
        print("Exiting...")
