import sys
import select
import os
import logging
import argparse

from options import mainframe_opts
from features.listener import Listener
from features.speaker import Speaker
from src.commander import Commander
from src.timer import Timer

class Mainframe:
  def __init__(self, speaker):
    self.speaker = speaker

  def main(self, args):
    # heavy initialization time
    # will be replaced by net
    self.speaker.write('Initializing Core...')
    commander = Commander(self.speaker)
    self.speaker.tell("γνῶθι σεαυτόν")

    while True:
      if args.private:
        print('AI/ORACLE>>> ', end='')
        speech = input()
      else:
        listener = Listener()
        speech = listener.mic_input()

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

