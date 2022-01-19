import pandas as pd
import chardet
import csv
# WIP
class Emailer:
  def __init__(self, speaker):
    self.speaker = speaker

  def read(self):
    with open('data/Velory_emails.csv') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      line_count = 0
      for row in csv_reader:
        if line_count == 0:
          print(f'Column names are {", ".join(row)}')
          line_count += 1
        else:
          print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
          line_count += 1
      print(f'Processed {line_count} lines.')

  def preprocess(self):
    csvfile = open('data/Velory_emails.csv', 'r').readlines()
    filename = 1
    for i in range(len(csvfile)):
      lang = chardet.detect(csvfile[i])
      print(lang)
      # if lang['encoding'] == 'EUC-JP':
        # open('JP' + str(filename) + '.csv', 'w+').writelines(csvfile[i])

      # filename += 1

  def map(self):
    emails = pd.read_csv('data/Velory_emails.csv', encoding='cp866')
    print(emails.shape)
