import sys
import re
import multiprocessing
import logging
from features.speaker import Speaker
from features.radio import Radio
from features.searcher import Searcher
from features.writer import Writer
from features.performer import Performer

class Mainframe:
  def __init__(self):
    self.speaker = Speaker()

  def speak(self, text, app_name='mainframe'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)
    self.speaker.text2speech(text)

  def write(self, text, app_name='mainframe'):
    logging.basicConfig(filename=f'logs/{app_name}.log', encoding='utf-8', level=logging.INFO)
    logging.info(text)

  def main(self):
    self.write(text='-------------------------------------------------------------')
    self.speak(text="γνῶθι σεαυτόν")

    while True:
      speech = self.speaker.mic_input()

      # should be replaced by neural net
      if re.search('oracle', speech):
        self.speak(f'Yes.')

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

      if re.search('tell weather', speech):
        Radio().weather()

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
      if re.search('open|create file', speech):
        fname = speech.split('file')[-1].strip()
        Writer().file_open(fname)

      if re.search('write in file', speech):
        Writer().file_write(speech) # not working that good

      if re.search('close file', speech):
        Writer().close_file()

      # ---
      # performer section
      #
      if re.search('open|launch|start application', speech):
        app_name = speech.split('application')[-1].strip()
        Performer().launch(app_name)

      # ---
      # utils section
      #
      if re.search('stop|finish|shutdown', speech):
        self.speak('Exiting. Good bye.')
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
