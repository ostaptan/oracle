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

import src.utils as utils

class Mainframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.bs_cmd = BasicCommander(speaker)
    self.sys_name = os.getcwd().split('/')[2]

    self.speaker.write('Connecting Core...')
    try:
      # self.ws = websocket.create_connection("ws://3.66.79.167:8000/")
      # self.ws = websocket.create_connection("ws://192.168.0.102:8000/")
      self.ws = websocket.create_connection("ws://127.0.0.1:8000/")
    except ConnectionRefusedError:
      self.speaker.tell('Cannot connect to core. Only basic support.')


  def main(self, args):
    self.speaker.tell('γνῶθι σεαυτόν!')

    while True:
      if args.private:
        print('CLI/ORACLE>>> ', end='')
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
            request = {
              'sysname': self.sys_name,
              'city': utils.get_city(),
              'speech': speech
            }
            self.ws.send(json.dumps(request))
            result = self.ws.recv()
            resj = json.loads(result)
            evaluat = eval(f'self.{resj["feature"]}.{resj["action"]}')
            evaluat(resj["data"])
          except websocket._exceptions.WebSocketConnectionClosedException:
            self.speaker.tell('Core error')
          except TypeError:
            self.speaker.tell('Unknown error')
          except AttributeError:
            self.speaker.tell('Cannot connect to core.')



if __name__ == "__main__":
  speaker = Speaker('mainframe')
  speaker.write('-------------------------------------------------------------')
  parser = argparse.ArgumentParser()
  mainframe_opts(parser)
  args = parser.parse_args()
  mf = Mainframe(speaker)
  speaker.write('Mainframe initialized.')
  mf.main(args)

