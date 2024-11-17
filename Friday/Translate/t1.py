import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from gtts import gTTS
import os

def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return None

def detect_language(text):
    try:
        language = detect(text)
        print("Detected language:", language)
        return language
    except:
        print("Language detection failed.")
        return None

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text
    print("Translated text:", translated_text)
    return translated_text

def text_to_speech(text, language):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")
    os.system("start output.mp3")

def main():
    input_text = recognize_speech()
    if input_text:
        input_language = detect_language(input_text)
        if input_language:
            target_language = input("Enter the language code for translation (e.g., 'es' for Spanish): ")
            translated_text = translate_text(input_text, target_language)
            text_to_speech(translated_text, target_language)

if __name__ == "__main__":
    main()
