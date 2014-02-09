import sys
import csv
import re

fields_name = ["client_ip", "timestamp", "http_first_line", "http_status", "response_size",
               "referrer_url", "user_agent", "time_respond"]

header = ["Date, ", "Expand Time"]

file_size = 0
fields_dict = dict()


def load_sections(filename):
  region_file = open(filename, 'rU')
  index = 0

  for x in fields_name:
    fields_dict[fields_name[index]] = []
    index += 1
  
  for line in region_file:
    line = line.strip()
    fields = re.split("[\s]+", line)

    fields_dict["client_ip"].append(fields[0])
    fields_dict["timestamp"].append(fields[3])
    fields_dict["http_first_line"].append(fields[5] + " " + fields[6] + " " + fields[7])
    fields_dict["http_status"].append(fields[8])
    fields_dict["response_size"].append(fields[9])
    
  region_file.close()
  return

# list dictionary in list mode
def print_dict_list_mode(my_dict):
  for field in fields_name:
    print field, ": " ,my_dict[field]
  return

def get_expand_time(my_dict):
  urls = my_dict["http_first_line"]
  count = 0
  for url in urls:
    search_url = "logevent?eventName=expandspdocframe"
    if url.find(search_url) != -1:
      count += 1
    else:
      continue
  return count


def main_helper():
  print str(get_expand_time(fields_dict))
  return


def main():

  header_str = ""
  for item in header:
    header_str += item
  print header_str

  for arg in sys.argv[1:]:
    load_sections(arg)
    tmp_str = arg.split('.')[-1]
    sys.stdout.write(tmp_str[0:2] + "-" + tmp_str[2:4] + "-" + tmp_str[4:6] + ", ")
    main_helper()

main();