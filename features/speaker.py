import speech_recognition as sr
import pyaudio
import random
import os
import time
from gtts import gTTS
from playsound import playsound
import sys
sys.path.append("./src")
from mic_recognizer import SpeechRecognition

class Speaker:
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

  def text2speech(self, text, lang='en'):
    """
    Convert any text to speech
    :param text: str
        text (String)
    :param lang: str
        default 'en'
    :return: Bool
        True / False (Play sound if True otherwise write exception to log and return False)
    """
    try:
      myobj = gTTS(text=text, lang=lang, slow=False)
      filename_str = '-'.join(text.split(' ')[:3])
      print(filename_str)
      filename_ascii = '.'.join(str(ord(c)) for c in filename_str) + '_' + time.strftime("%d%m%Y%H%M%S")
      myobj.save(f'sounds/{filename_ascii}')
      playsound(f'sounds/{filename_ascii}')
      # os.remove("tmp.mp3")
      return True
    except Exception as e:
      mytext = "Sorry I couldn't understand."
      print(mytext)
      myobj = gTTS(text=mytext, lang=lang, slow=False)
      myobj.save("tmp.mp3")
      playsound("tmp.mp3")
      os.remove("tmp.mp3")
      print(e)
      return False
