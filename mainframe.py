import sys
import select
import os
import json
import logging
import argparse

from options import mainframe_opts
from features.listener import Listener
from features.speaker import Speaker
from src.basic_commander import BasicCommander

from websocket import create_connection

class Mainframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.bs_cmd = BasicCommander(speaker)
    self.ws = create_connection("ws://127.0.0.1:8000/")

  def __notify(self, title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"' with timeout of 86400 seconds end timeout
              """.format(text, title))

  def greeting(self):
    sys_name = os.getcwd().split('/')[2]
    text = f'Welcome, master {sys_name}!'
    self.__notify('γνῶθι σεαυτόν!', text)
    self.speaker.tell(text)

  def main(self, args):
    self.speaker.write('Connecting Core...')

    self.greeting()

    while True:
      if args.private:
        print('AI/ORACLE>>> ', end='')
        speech = input()
      else:
        listener = Listener()
        speech = listener.mic_input()

      if speech:
        if self.bs_cmd.do(speech):
          pass
        else:
          # send ws command to core
          self.ws.send(speech)
          result =  self.ws.recv()
          resj = json.loads(result)
          evaluat = eval(f'self.{resj["feature"]}.{resj["action"]}')
          evaluat(resj["data"])


if __name__ == "__main__":
  speaker = Speaker('mainframe')
  speaker.write('-------------------------------------------------------------')
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe(speaker)
  speaker.write('Mainframe initialized.')
  mf.main(args)

