import os
import sys
import time
import random
# import pyaudio
import speech_recognition as sr

from src.mic_recognizer import SpeechRecognition

class Listener:
  def __init__(self):
    self.speech_recognition_ai = SpeechRecognition()

  def mic_input(self, lang='en'):
    """
    Fetch input from mic
    Note: mic_input usages Google's Speech Recognition
    Limitation: After multiple hits API may not work so use mic_input_ai() instead of mic_input
    :param lang: str
        default 'en'
    :return: str/Bool
        user's voice input as text if true/ false if fail
    """

    try:
      r = sr.Recognizer()
      with sr.Microphone() as source:
        print("Speak...")
        os.system("""
              osascript -e 'display notification "{}" with title "{}"' with timeout of 86400 seconds end timeout
              """.format('Speak ...', 'Oracle'))
        r.pause_threshold = 1
        r.dynamic_energy_threshold = True
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
      try:
          command = r.recognize_google(audio, language=lang).lower()
          print('You said: ' + command + '\n')
      except sr.UnknownValueError:
          print('....')
          command = self.mic_input()
      return command
    except Exception as e:
      print(e)
      return False

  def mic_input_ai(self, record_seconds=5, debug=False):
    """
    Fetch input from mic and recognition using Transformers
    Note: This will download pretrained ML model for the first time only
    :param record_seconds: int
        Default 5
    :param debug: bool
        Print recording status if True
    :return: str
        User's voice input as text
    """
    transcription = self.speech_recognition_ai.start_speech_recognition(record_seconds=record_seconds, debug=debug)
    return transcription

