import sys
import re

fields_name = ["timestamps", "program_name", "product_SKU", "request_type",
               "request_url", "client_ip", "query", "request_service", "resource_type",
               "resource_id", "description", "result_count", "response_code",
               "response_time", "user_id", "user_account", "group_account",
               "library_card", "referer_url", "thread_id", "session_id", "search_id",
               "request_id", "content_length", "session_sequence", "grade",
               "user_role", "server", "hostname", "owner_id", "search_mode",
               "delivery_method", "access_method", "selling_method", "contract_type",
               "delivery_format", "document_source", "dumy1", "content_type",
               "authentication_method", "language", "interface_type", "dumy2",
               "subscription_id", "usage_type", "user_agent"]

file_size = 0
fields_dict = dict()

def load_sections(filename):
  region_file = open(filename, 'rU')
  index = 0
  #create a list for each field
  for x in fields_name:
    fields_dict[fields_name[index]] = []
    index += 1
  index = 0
  
  for line in region_file:
    fields = line.split(";;|")
    #add each line of log files into each fields list
    for field in fields:
      fields_dict[fields_name[index]].append(field) # field
      index += 1

    index = 0
  region_file.close()
  return


# list dictionary in list mode
def print_dict_list_mode(my_dict):
  for field in fields_name:
    print field, ": " ,my_dict[field]
  return

 
def print_requests_per_hour(my_dict):
  requests_per_hour = dict()
  for i in range(0, 24):
    requests_per_hour[i] = 0 
  
  for my_timestamp in my_dict["timestamps"]:
    x = int(my_timestamp.split(" ")[3].split(":")[0])
    requests_per_hour[x] += 1
  
  for requests_index in requests_per_hour:
    print requests_index, requests_per_hour[requests_index]

  return


def print_avg_time_view_doc(my_dict):
  avg_time_info = dict()

  for i in range(0, len(my_dict)):
    my_hostname = fields_dict["hostname"][i]
    if my_hostname == "":
      continue

    if my_hostname in avg_time_info:
      add_time = 0
      if fields_dict["response_time"][i] != "":
        add_time = int(fields_dict["response_time"][i])
        
      avg_time_info[my_hostname][0] += add_time
      avg_time_info[my_hostname][1] += 1 
    else:
      temp_info = []
      init_time = 0
      if fields_dict["response_time"][i] != "":
        init_time = int(fields_dict["response_time"][i])
      temp_info.append(init_time)
      temp_info.append(1)
      avg_time_info[my_hostname] = temp_info

  for item in avg_time_info:
    print item, float(avg_time_info[item][0])/avg_time_info[item][1], avg_time_info[item][1]
  return

def get_search_times(my_dict):
  urls = my_dict["request_url"]
  count = 0
  for url in urls:
    search_url = "do/results"
    if url.find(search_url) != -1:
      count += 1
    else:
      continue
  return count

def get_research_topic_click(my_dict):
  urls = my_dict["request_url"]
  count = 0
  for url in urls:
    search_url = "do/issuebrowsenew"
    if url.find(search_url) != -1:
      count += 1
    else:
      continue
  return count

def main():
  #load_sections("sample_logfile.txt")
  for arg in sys.argv:
    load_sections(arg)
  #print_avg_time_view_doc(fields_dict["timestamps"])
  #print_requests_per_hour(fields_dict)
  #print_dict_list_mode(fields_dict)
  print get_research_topic_click(fields_dict)
main();
