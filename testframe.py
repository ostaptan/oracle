from features.speaker import Speaker
from features.searcher import Searcher

class Testframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.searcher = Searcher(speaker)

  def test(self):
    q = 'neural text classifier'
    q1 = 'sunset in lviv today'
    q2 = 'what is javascript'
    q3 = 'star wars episode 8'
    self.searcher.google(q3)



speaker = Speaker('testframe')
speaker.write('-------------------------------------------------------------')
tf = Testframe(speaker)
tf.test()
