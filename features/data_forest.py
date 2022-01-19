import os

class DataForest:
  def __init__(self, speaker):
    self.speaker = speaker

  def classify(self, sb_dir):
    self.sandbox_dir = sb_dir

  def rec_map(self, karta, way):
    donePaths = []
    stats = {}

    for path, dirs, files in os.walk(way):
      if path not in donePaths:
        depth = path.count('/') - 3
        if files:
          for fl_name in files:
            ext = fl_name.split('.')[-1]
            if ext in stats:
              stats[ext] += 1
            else:
              stats[ext] = 1

            karta[fl_name] = {
              'ext': ext,
              'depth': depth,
              'path': path
            }
        if dirs:
          for dr_name in dirs:
            if 'folder' in stats:
              stats['folder'] += 1
            else:
              stats['folder'] = 1

            karta[dr_name] = {
              'ext': 'folder',
              'depth': depth,
              'path': path
            }



            # absPath = os.path.join(path, dr)
            # # recursively calling the map function on each directory
            # self.rec_map(karta, absPath)
            # # adding the paths to the list that got traversed
            # donePaths.append(absPath)
    return karta, stats
