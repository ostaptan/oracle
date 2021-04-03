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
  def __init__(self):
    self.listener = Listener()
    self.speaker = Speaker('mainframe')

  def main(self, args):
    self.speaker.write('-------------------------------------------------------------')
    self.speaker.tell("γνῶθι σεαυτόν")
    commander = Commander()

    while True:
      if args.private:
        print('O>>> ')
        i, o, e = select.select([sys.stdin], [], [], 33)

        if (i):
          speech = sys.stdin.readline().strip()
        else:
          # 60 sec timeout going to sleep
          commander.do('sleep')
      else:
        speech = self.listener.mic_input()

      commander.do(speech)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe()
  mf.main(args)

