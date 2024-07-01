import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import subprocess
import json

# Pygame????
pygame.mixer.pre_init(buffer=64)
pygame.init()
screen = pygame.display.set_mode((100, 100))

# ??????
def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)
        
    try:
        response = recognizer.recognize_google(audio, language='ja-JP')
    except sr.RequestError:
        response = "API unavailable"
    except sr.UnknownValueError:
        response = "Unable to recognize speech"
    
    return response

# OpenAI API?????????
def generate_response(prompt, past_messages=[]):
    result = subprocess.run(
        ['node', 'api.js', prompt, json.dumps(past_messages)],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"Node.js script error: {result.stderr}")

    response_data = json.loads(result.stdout)
    return response_data['responseMessage'], response_data['pastMessages']

# ??????????????
def text_to_speech(text):
    tts = gTTS(text=text, lang='ja')
    filename = "response.mp3"
    tts.save(filename)

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        continue

    os.remove(filename)

def main():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    past_messages = []
    is_execution = False

    print("Press '1' (NumPad) to start speaking, press '3' (NumPad) to stop...")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP1:
                    is_execution = True
                    print("Starting conversation...")
                elif event.key == pygame.K_KP3:
                    is_execution = False
                    print("Stopping conversation.")
                    break

        while is_execution:
            print("Say something:")
            speech = recognize_speech_from_mic(recognizer, microphone)
            print(f"You said: {speech}")

            if "ããã" in speech:
                print("Stopping conversation.")
                is_execution = False
                break

            response, past_messages = generate_response(speech, past_messages)
            print(f"Response: {response}")
            text_to_speech(response)

            # ???????????????'3'?????????????
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP3:
                        print("Stopping conversation.")
                        is_execution = False
                        break

        pygame.display.update()

if __name__ == "__main__":
    main()

