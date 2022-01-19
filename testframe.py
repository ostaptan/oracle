import json
from features.speaker import Speaker
from features.data_forest import DataForest

class Testframe:
  def __init__(self, speaker):
    self.speaker = speaker
    self.data_forest = DataForest(speaker)

  def test(self):
    working_dir = '/Users/ostap.ivanyshyn/Downloads'
    fmap, stats = self.data_forest.rec_map({}, working_dir)
    print(f'Files Map: ({len(fmap)})')
    print(stats)
    # print(json.dumps(fmap, indent=4, sort_keys=False))

speaker = Speaker('testframe')
speaker.write('-------------------------------------------------------------')
tf = Testframe(speaker)
tf.test()
