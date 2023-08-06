import sys
import select
import json
import logging
import argparse
import websocket

from options import mainframe_opts
# from features.listener import Listener
from features.speaker import Speaker
from features.radio import Radio
from src.commander import Commander

class Mainframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.radio = Radio(speaker)

  def main(self, args):
    self.speaker.write('Initializing Core...')
    commander = Commander(self.speaker)
    self.radio.greeting()
    # must say current name
    # compose name from mm/cw/r/names data
    # first dummy neural net integration

    while True:
      # if args.private:
      print('/> ', end='')
      speech = input()
      # else:
      #   listener = Listener()
      #   speech = listener.mic_input()

      # believe in yourself and let the force be with u
      if speech:
        commander.do(speech)

if __name__ == "__main__":
  speaker = Speaker('mainframe')
  speaker.write('-------------------------------------------------------------')
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe(speaker)
  speaker.write('Mainframe initialized.')
  mf.main(args)

