import sys
import os
import logging
import argparse

from options import mainframe_opts
from features.listener import Listener
from features.speaker import Speaker
from src.commander import Commander
from src.timer import Timer

class Mainframe:
  def __init__(self):
    self.listener = Listener()
    self.speaker = Speaker('mainframe')

  def main(self, args):
    self.speaker.write('-------------------------------------------------------------')
    self.speaker.tell("γνῶθι σεαυτόν")
    commander = Commander()
    t = Timer()
    t.start()

    while True:
      if args.private:
        speech = input('O>>> ')
      else:
        speech = self.listener.mic_input()

      time_el = t.check()
      if time_el > 120.0:
        t.stop()
        commander.do('sleep')

      commander.do(speech)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe()
  mf.main(args)

