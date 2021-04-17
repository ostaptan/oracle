import sys
import select
import os
import json
import logging
import argparse
import websocket

from options import mainframe_opts
from features.listener import Listener
from features.speaker import Speaker
from src.basic_commander import BasicCommander

class Mainframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.bs_cmd = BasicCommander(speaker)
    # self.ws = websocket.create_connection("ws://192.168.0.102:8000/")
    self.ws = websocket.create_connection("ws://127.0.0.1:8000/")

  def main(self, args):
    self.speaker.write('Connecting Core...')
    self.speaker.tell('γνῶθι σεαυτόν!')

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
          try:
            self.ws.send(speech)
            result = self.ws.recv()
            resj = json.loads(result)
            evaluat = eval(f'self.{resj["feature"]}.{resj["action"]}')
            evaluat(resj["data"])
          except websocket._exceptions.WebSocketConnectionClosedException:
            self.speaker.tell('Core error')
          except TypeError:
            self.speaker.tell('Unknown error')



if __name__ == "__main__":
  speaker = Speaker('mainframe')
  speaker.write('-------------------------------------------------------------')
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe(speaker)
  speaker.write('Mainframe initialized.')
  mf.main(args)

