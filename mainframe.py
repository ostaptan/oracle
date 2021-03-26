import sys
import re
import os
import multiprocessing
import logging
import notify2

from features.listener import Listener
from features.speaker import Speaker
from features.radio import Radio
from features.searcher import Searcher
from features.writer import Writer
from features.conductor import Conductor

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

  def main(self):
    self.__write('-------------------------------------------------------------')
    self.__speak("γνῶθι σεαυτόν")

    while True:
      speech = self.listener.mic_input()

      # should be replaced by neural net
      if re.search('oracle|hello|hey|', speech):
        self.__speak('Yes.')

      # ---
      # radio section
      #
      if re.search('radio', speech):
        Radio().scenario()

      if re.search('tell a joke', speech):
        Radio().joke()

      if re.search('what|tell time', speech):
        Radio().datetime_now()

      if re.search('tell aphorism|quote', speech):
        Radio().aphorism()

      if re.search('a poem', speech):
        Radio().poem()

      if re.search('tell weather', speech):
        Radio().weather()

      if re.search('dialectica', speech):
        Radio().read_dial()

      # ---
      # searcher section
      #
      if re.search('wiki|find about', speech):
        topic = speech.split('about')[-1].strip()
        Searcher().wiki(topic)

      if re.search('tell news', speech):
        Searcher().local_news()

      # WORLD NATION BUSINESS TECHNOLOGY ENTERTAINMENT SPORTS SCIENCE HEALTH
      if re.search('tell news about', speech):
        topic = speech.split('about')[-1].strip()
        Searcher().topic_news(topic.upper())

      # ---
      # writer section
      # must have shared memory to operate in one file
      # still not working without net
      #
      # not need to name files ))

      # if re.search('open|create file', speech):
      #   fname = speech.split('file')[-1].strip()
      #   Writer().file_open(fname)

      if re.search('fix', speech):
        Writer().mustdo(speech)

      #
      ###

      #
      #
      ##
      #
      #

      recent_rec = Writer().recent_file()
      if recent_rec and recent_rec.opened:
        f = open(recent_rec.path, 'a+')
        f.write(f, speech + "\n")

        if re.search('end', speech):
          Writer().wclose(f)

      # ---
      # conductor section
      #
      if re.search('open|launch|start application', speech):
        app_name = speech.split('application')[-1].strip()
        Conductor().launch(app_name)

      if re.search('unlock', speech):
        Conductor().unlock('MUSTDO')

      if re.search('lock', speech):
        Conductor().lock('MUSTDO')


      # ---
      # utils section
      #
      if re.search('stop|finish|shutdown', speech):
        self.__speak('Exiting. Good bye.')
        sys.exit()


# schedule.every().hour.do(Mainframe().main())
# schedule.every().hour.do(main)
# schedule.every().hour.do(main)

if __name__ == "__main__":
  mf = Mainframe()
  mf.main()

  # while True:
  #   schedule.run_pending()
  #   time.sleep(1)
