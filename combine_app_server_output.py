import sys
import csv
import re

header = ["Date, ", "Search Count, ", "Research Topic Click"]
binder_date = []

binder = dict()

def init_sections(filename):
  region_file = open(filename, 'rU')
  
  skip = 0

  for line in region_file:
    if skip == 0:
      skip = 1
      continue
    fields = line.split(",")
    binder[fields[0]] = [0, 0]
    binder_date.append(fields[0])
  return

def load_sections(filename):

  region_file = open(filename, 'rU')
  region_file.seek(0)

  skip = 0
  for line in region_file:
    if skip == 0:
      skip = 1
      continue
    fields = line.split(",")

    binder[fields[0]][0] += int(fields[1])
    #print fields[0], binder[fields[0]][0], int(fields[1])

    binder[fields[0]][1] += int(fields[2].split("\n")[0])
  
  region_file.close()
  return


def print_binder():
  for item in binder_date:
    print item, ",", binder[item][0], "," ,binder[item][1]


def main():

  for item in header:
    sys.stdout.write(item)
  print("")

  init_dict = True
  for arg in sys.argv[1:]:
    #sys.stdout.write(arg.split('.')[-1] + ", ")
    if init_dict:
      init_sections(arg)
      init_dict = False

    load_sections(arg)
  
  print_binder()

main();