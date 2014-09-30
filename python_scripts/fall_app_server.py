import sys
import csv
import re
import os

fields_name = ["timestamps", "program_name", "product_SKU", "request_type", "request_url", "client_ip", "query", "request_service", "resource_type",
               "resource_id", "description", "result_count", "response_code", "response_time", "user_id", "user_account", "group_account",
               "library_card", "referer_url", "thread_id", "session_id", "search_id", "request_id", "content_length", "session_sequence", "grade",
               "user_role", "server", "hostname", "owner_id", "search_mode", "delivery_method", "access_method", "selling_method", "contract_type",
               "delivery_format", "document_source", "dumy1", "content_type", "authentication_method", "language", "interface_type", "dumy2",
               "subscription_id", "usage_type", "user_agent"]

header = ["Date, ", "Search Count, ", "Research Topic Click"]

file_size = 0
session_dict = dict()
session_table = dict()

def load_sections(filename):
  region_file = open(filename, 'rU')
  index = 0
  
  for line in region_file:
    index = 0
    fields = line.split(";;|")
    session_id = fields[20]
    if session_id not in session_dict:
      session_dict[session_id] = dict()

    # add each line of log files into each fields list
    for field in fields:
      if fields_name[index] not in session_dict[session_id]:
        session_dict[session_id][fields_name[index]] = []
      session_dict[session_id][fields_name[index]].append(field)
      index += 1

  region_file.close()
  return


def get_total_search_counts(my_dict):
  session_search_counts = get_session_search_counts(my_dict)
  count = 0
  for session_id in session_search_counts:
    count += session_search_counts[session_id]       
  return count


def get_session_search_counts(my_dict):
  count = 0
  session_search_counts = {}
  for session_id in my_dict:
    if session_id not in session_search_counts:
      session_search_counts[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_type"]
    #for url in urls:
    for i in range (0,len(urls)):
      search_url1 = "/do/search"
      search_url2 = "POST"
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_search_counts[session_id] += 1

  return session_search_counts


def get_session_retrieval_counts(my_dict):
  count = 0
  session_retrieval_counts = {}
  for session_id in my_dict:
    if session_id not in session_retrieval_counts:
      session_retrieval_counts[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_service"]
    #for url in urls:
    for i in range (0,len(urls)):
      search_url1 = "/do/document"
      search_url2 = "SEARCH_DOC_RETRIEVAL;;Document"

      '''
      if types[i].find("SEARCH_DOC_RETRIEVAL;;") != -1 and types[i].find("SEARCH_DOC_RETRIEVAL;;Document") == -1:
        print types[i]
      '''

      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_retrieval_counts[session_id] += 1

  return session_retrieval_counts


def get_session_preview_counts(my_dict):
  count = 0
  session_preview_counts = {}
  for session_id in my_dict:
    if session_id not in session_preview_counts:
      session_preview_counts[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_service"]
    #for url in urls:
    for i in range (0,len(urls)):
      search_url1 = "/do/document"
      search_url2 = "SEARCH_DOC_RETRIEVAL;;DocumentPreview"
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_preview_counts[session_id] += 1

  return session_preview_counts


def get_total_preview_counts(my_dict):
  session_preview_counts = get_session_preview_counts(my_dict)
  count = 0
  for session_id in session_preview_counts:
    count += session_preview_counts[session_id]
  return count 


def get_total_retrieval_counts(my_dict):
  session_retrieval_counts = get_session_retrieval_counts(my_dict)
  count = 0
  for session_id in session_retrieval_counts:
    count += session_retrieval_counts[session_id]
  return count 


def get_research_topic_click(my_dict):
  count = 0
  for session_id in my_dict:
    urls = my_dict[session_id]["request_url"]  
    for url in urls:
      search_url = "do/issuebrowsenew"
      if url.find(search_url) != -1:
        count += 1
      else:
        continue
  return count

def get_mean_ratio_preview_over_retrieval(my_dict):
  mean = 0
  preview = get_session_preview_counts(my_dict)
  retrieval = get_session_retrieval_counts(my_dict)
  retrieval_count = 0;
  for session_id in my_dict:
    if retrieval[session_id] != 0:
      retrieval_count += 1
      mean += preview[session_id] * 1.0 / retrieval[session_id]

  mean /= retrieval_count
  return mean


def get_session_num(my_dict):
  return len(get_session_retrieval_counts(my_dict))


def load(file):
  session_table = dict()
  load_sections(file)
  session_retrieval_table = get_session_retrieval_counts(session_dict)
  session_preview_table = get_session_preview_counts(session_dict)
  session_search_table = get_session_search_counts(session_dict)

  for session in session_search_table:
    session_table[session] = dict()
    session_table[session]["search"] = session_search_table[session]

  for session in session_preview_table:
    session_table[session]["preview"] = session_preview_table[session]

  for session in session_retrieval_table:
    session_table[session]["retrieval"] = session_preview_table[session]

  return session_table


def main():
    '''
    header_str = ""
    #for item in header:
    #for item in header2:
    for item in header3:
        header_str += item
    print header_str

    print 

    #format: num_of_servers, server_names, 
    #generate list of servers: 101,102,...
    server_num = int(sys.argv[1])
    server_names = []
    for i in range (0, server_num):
        my_server = 101 + i
        server_names.append(str(my_server)) #list of str

    log_years = []
    for i in range(2, len(sys.argv)):
        log_years.append(sys.argv[i]) #list of str

    #generate dict of folder directory
    # year -> dir1, dir2,...,dir15
    file_prefix = 'elibrary.bigchalk.com-access_log.'
    dir_prefix = '/home/ec2-user/ummdp/logfiles/'
    year_servers = dict()  
    for year in log_years:
        year_servers[year] = []
        for i in server_names:
            temp = dir_prefix + i + "/apache_access/" + year + "/"
            year_servers[year].append(temp)

    for year in log_years:
        #for x in range(1,13):
        for x in range(1,2):
            month = "%02d" %(x)
            #for y in range (1,32):
            for y in range (1, 2):
                date = "%02d" %(y)
                #generate list of file dir for each day(one for each server)
                file_list = []
                for i in range (0, server_num):
                    file_list.append(year_servers[year][i] + file_prefix + year[2:] + month + date)
                load_a_day(file_list)
    '''

    file_path = '/Users/hongbo/Desktop/elibdmz-elibweb_usage.log.2013-12-03'
    if (os.path.exists(file_path)):
      load(file_path)

main();


