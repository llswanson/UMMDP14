import sys
import csv
import re
import os
# import pdb

fields_name = ["timestamps", "program_name", "product_SKU", "request_type", "request_url", "client_ip", "query", "request_service", "resource_type",
               "resource_id", "description", "result_count", "response_code", "response_time", "user_id", "user_account", "group_account",
               "library_card", "referer_url", "thread_id", "session_id", "search_id", "request_id", "content_length", "session_sequence", "grade",
               "user_role", "server", "hostname", "owner_id", "search_mode", "delivery_method", "access_method", "selling_method", "contract_type",
               "delivery_format", "document_source", "dumy1", "content_type", "authentication_method", "language", "interface_type", "dumy2",
               "subscription_id", "usage_type", "user_agent"]

file_size = 0
session_dict = dict()
session_table = dict()

def load_sections(filename):
  region_file = open(filename, 'rU')
  index = 0
  
  for line in region_file:
    index = 0
    fields = line.split(";;|")
    if (len(fields) >= 20):
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

def get_session_search_counts(my_dict):
  count = 0
  session_search_counts = {}
  for session_id in my_dict:
    if session_id not in session_search_counts:
      session_search_counts[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_service"]
    search_url1 = "/do/search"
    search_url2 = "SEARCH_SEARCH"
    
    #print len(urls)  
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1:
        if i < len(types) and types[i].find(search_url2) != -1:
            session_search_counts[session_id] += 1

  return session_search_counts


def get_session_retrieval_counts(my_dict):
  count = 0
  session_retrieval_counts = {}
  session_retrieval_from_search = {}
  for session_id in my_dict:
    if session_id not in session_retrieval_counts:
      session_retrieval_counts[session_id] = 0
      session_retrieval_from_search[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_service"]
    queries = my_dict[session_id]["query"]
    search_url1 = "/do/document"
    search_url2 = "SEARCH_DOC_RETRIEVAL;;Document"
    search_url3 = "set=search"
    
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_retrieval_counts[session_id] += 1
        if queries[i].find(search_url3) != -1:
            session_retrieval_from_search[session_id] += 1

  return session_retrieval_counts, session_retrieval_from_search

def get_session_preview_counts(my_dict):
  count = 0
  session_preview_counts = {}
  session_preview_from_search = {}
  for session_id in my_dict:
    if session_id not in session_preview_counts:
      session_preview_counts[session_id] = 0
      session_preview_from_search[session_id] = 0

    urls = my_dict[session_id]["request_url"]
    types = my_dict[session_id]["request_service"]
    queries = my_dict[session_id]["query"]
    search_url1 = "/do/document"
    search_url2 = "SEARCH_DOC_RETRIEVAL;;DocumentPreview"
    search_url3 = "set=search"

    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_preview_counts[session_id] += 1
        if queries[i].find(search_url3) != -1:
            session_preview_from_search[session_id] += 1

  return session_preview_counts, session_preview_from_search


def get_total_search_counts(my_dict):
  session_search_counts = get_session_search_counts(my_dict)
  count = 0
  for session_id in session_search_counts:
    count += session_search_counts[session_id]       
  return count

'''
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
'''

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

'''
def get_mean_rs_ratio_preview_over_retrieval(my_dict):
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
'''

def load(file):
  session_table = dict()
  load_sections(file)
  session_retrieval_table, session_retrieval_from_search = get_session_retrieval_counts(session_dict)
  session_preview_table, session_preview_from_search = get_session_preview_counts(session_dict)
  session_search_table = get_session_search_counts(session_dict)
  search_count = get_total_search_counts(session_dict)
  research_topic_click = get_research_topic_click(session_dict)
  session_dict.clear()
  #print "search count " + str(search_count) + ",  r-click " + str(research_topic_click)
  session_search_table.clear()
  session_retrieval_table.clear()
  session_preview_table.clear()
  session_retrieval_from_search.clear()
  session_preview_from_search.clear()
  session_table.clear()

  return {"search_count": search_count, "r_click": research_topic_click} 

def main():
    file_list_prefix = "/home/ec2-user/UMMDP14/2014_d/app_server" 
    app_server= dict()
    dates = set()
    for i in range(101, 116):
        file_list_name = file_list_prefix + str(i)
        app_server[i] = dict()
        app_server[i]['file_list'] = open(file_list_name, 'rU')
        app_server[i]['files'] = dict()
        for filename in app_server[i]['file_list']:
            filename = filename.rstrip('\n')
            date = filename.split(".")[2]
            dates.add(date)
            app_server[i]['files'][date] = filename
        app_server[i]['file_list'].close()
 
    ordered_date = list(dates)
    ordered_date.sort()

    

    filtered_date_1308 = get_dates(ordered_date, "2013", "08")
    filtered_date_1408 = get_dates(ordered_date, "2014", "08")
    filtered_date_1309 = get_dates(ordered_date, "2013", "09")
    filtered_date_1409 = get_dates(ordered_date, "2014", "09")

    date_lists = {"1308": filtered_date_1308, "1309": filtered_date_1309, "1408": filtered_date_1408, "1409": filtered_date_1409}

    write_file_prefix = '/home/ec2-user/UMMDP14/compare/'
    comma = ','
    newline = '\n'
    
    search_counts = 0
    r_click_counts = 0


    for key, date_list in date_lists.iteritems():
    
        for date in date_list:
            # get session table for a day
            for i in range(101, 116):
                if date in app_server[i]['files']:
                    path = app_server[i]['files'][date]
                    if (os.path.exists(path)):
                        #print path
                        res = load(path)
                        search_counts += res["search_count"]
                        r_click_counts += res["r_click"]
                else:
                    continue
            
        write_filename = write_file_prefix + key
        output_file = open(write_filename, 'w+')
        output_file.write("" + newline)

        output_file.write("search count: " + str(search_counts) + newline)
        output_file.write("research_topic click: " + str(r_click_counts) + newline)
        print key + " search: " + str(search_counts) + ", " + str(r_click_counts)

        output_file.close()

    return


def get_dates(date_list, year, month):
    filtered_set = set()
    filtered_list = list()
    for date in date_list:
        date_fields = date.split("-")
        if (date_fields[0] == year and date_fields[1] == month):
            filtered_list.append(date)

    filtered_set = list(filtered_list)
    filtered_set.sort()    
    return filtered_set 

'''
def test():
    test_file = '/home/ec2-user/ummdp/logfiles/101/app/2013/elibdmz-elibweb_usage.log.2013-01-01'
    # check the output of session_dict, confirmed that all urls are packed in a list 
    # needs to iterate through the list to get precise search count 
    # similarly for retrieval and preview

    load_sections(test_file)
    print session_dict

    # check the output for all zero sessions 
    # confirmed that GET request is also used for /do/search
    # should eliminate POST checker for get search count
    output = load(test_file)
    for key,value in output.iteritems():
        if (value['search'] == 0 and value['retrieval'] == 0 and value['preview'] == 0):
            print session_dict                
    return
'''
main();
#test();

