import openai
import speech_recognition as sr
import pyttsx3

# Initialize OpenAI API
openai.api_key = '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'

# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

def generate_response(prompt):
    # Call OpenAI API to generate response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    return response.choices[0].text.strip()

def speech_to_text():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I didn't get that.")
        return ""
    except sr.RequestError:
        print("Sorry, I couldn't request results. Please check your internet connection.")
        return ""

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Listen for user input
        user_input = speech_to_text()
        
        # Generate response using GPT-3
        response = generate_response(user_input)
        
        # Convert response to speech and play it back
        text_to_speech(response)

if __name__ == "__main__":
    main()
