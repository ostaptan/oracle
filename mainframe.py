import sys
import os
import logging
import argparse

from options import mainframe_opts
from features.listener import Listener
from features.speaker import Speaker
from src.commander import Commander

class Mainframe:
  def __init__(self):
    self.listener = Listener()
    self.speaker = Speaker()

  def __speak(self, text, app_name='mainframe'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def __write(self, text, app_name='mainframe'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)

  def main(self, args):
    self.__write('-------------------------------------------------------------')
    self.__speak("γνῶθι σεαυτόν")
    commander = Commander()

    while True:
      if args.private:
        print('>>> Type...')
        speech = input()
      else:
        speech = self.listener.mic_input()

      commander.do(speech)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe()
  mf.main(args)

