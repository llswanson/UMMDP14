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
    else: 
        print "Error @ " + filename + line
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
      
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
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

def get_session_addtomylist_counts(my_dict):
    # count all the files that are added to mylist
    # without specifying if is a regular doc or research topic
    count = 0
    session_addtomylist_counts = {}
    for session_id in my_dict:
        if session_id not in session_addtomylist_counts:
           session_addtomylist_counts[session_id] = 0
        urls = my_dict[session_id]["request_url"]
        types = my_dict[session_id]["request_service"]
        queries = my_dict[session_id]['query']
        search_url1 = '/do/mylist'
        search_url2 = 'MyListComponent'
        search_url3 = 'mylist=add'

    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1 and queries[i].find(search_url3) != -1:
           session_addtomylist_counts[session_id] += 1

    return session_addtomylist_counts 
       
def get_session_email_counts(my_dict):
    count = 0
    session_email_counts = {}
    for session_id in my_dict:
        if session_id not in session_email_counts:
           session_email_counts[session_id] = 0
        urls = my_dict[session_id]["request_url"]
        queries = my_dict[session_id]['query']
        search_url1 = '/do/email'
        search_url2 = 'set=search'

    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and queries[i].find(search_url2) != -1:
           session_email_counts[session_id] += 1

    return session_email_counts 

def get_session_print_counts(my_dict):
    count = 0
    session_print_counts = {}
    for session_id in my_dict:
        if session_id not in session_print_counts:
           session_print_counts[session_id] = 0
        urls = my_dict[session_id]["request_url"]
        queries = my_dict[session_id]['query']
        search_url1 = '/do/document'
        search_url2 = 'set=search'
        search_url3 = 'style=printable'

    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and queries[i].find(search_url2) != -1 and queries[i].find(search_url3) != -1:
           session_print_counts[session_id] += 1

    return session_print_counts 
 
def load(file):
  session_table = dict()
  load_sections(file)
  session_retrieval_table, session_retrieval_from_search = get_session_retrieval_counts(session_dict)
  session_preview_table, session_preview_from_search = get_session_preview_counts(session_dict)
  session_search_table = get_session_search_counts(session_dict)
  session_addtomylist_table = get_session_addtomylist_counts(session_dict)
  session_email_table = get_session_email_counts(session_dict)
  session_print_table = get_session_print_counts(session_dict)
  session_dict.clear()
    
  for session in session_search_table:
    session_table[session] = dict()
    session_table[session]["search"] = session_search_table[session]

  for session in session_preview_table:
    session_table[session]["preview"] = session_preview_table[session]

  for session in session_preview_from_search:
    session_table[session]["preview_from_search"] = session_preview_from_search[session]

  for session in session_retrieval_table:
    session_table[session]["retrieval"] = session_retrieval_table[session]

  for session in session_retrieval_from_search:
    session_table[session]["retrieval_from_search"] = session_retrieval_from_search[session]

  for session in session_addtomylist_table:
    session_table[session]['addtomylist'] = session_addtomylist_table[session]

  for session in session_email_table:
    session_table[session]['email'] = session_email_table[session]

  for session in session_print_table:
    session_table[session]['print'] = session_print_table[session]

  session_search_table.clear()
  session_retrieval_table.clear()
  session_preview_table.clear()
  session_retrieval_from_search.clear()
  session_preview_from_search.clear()
  session_addtomylist_table.clear()
  session_email_table.clear()
  session_print_table.clear()
 
  return session_table

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

    write_file_prefix = '/home/ec2-user/UMMDP14/app_server_parsed/'
    comma = ','
    newline = '\n'
    for date in ordered_date:
        # write session table to a file
        write_filename = write_file_prefix + date
        output_file = open(write_filename, 'w+')
        header_str = "session_id,date,search,retrieval,retrieval_from_search,preview,preview_from_search,rs_ratio,add_to_my_list,email,print" 
        output_file.write(header_str + newline)

        # get session table for a day
        for i in range(101, 116):
            path = app_server[i]['files'][date]
            if (os.path.exists(path)):
                session_table_for_server_i = load(path) 
            for key, value in session_table_for_server_i.iteritems():
                rs_ratio = 0  # rs_ratio of retrieval / search
                if value['search'] == 0:
                    rs_ratio = -1
                else:
                    total_retrieval_from_search =  value['retrieval_from_search'] + value['preview_from_search']
                    rs_ratio = total_retrieval_from_search / (value['search'] * 1.0) 
                output_file.write(key + comma + date + comma + str(value['search']) + comma + str(value['retrieval']) + comma + str(value['retrieval_from_search']) + comma + str(value['preview']) + comma +str(value["preview_from_search"]) + comma + str(rs_ratio) + comma + str(value['addtomylist']) + comma + str(value['email']) + comma + str(value['print']) + comma + newline)
           
                 # for collection purpose
                if (value['addtomylist'] != 0 or value['email'] != 0 or value['print'] != 0):
                    print 'Find satisfaction point @ ' + key + comma + date + comma + str(value['search']) + comma + str(value['retrieval']) + comma + str(value['retrieval_from_search']) + comma + str(value['preview']) + comma +str(value["preview_from_search"]) + comma + str(rs_ratio) + comma + str(value['addtomylist']) + comma + str(value['email']) + comma + str(value['print']) + comma + newline
            
            session_table_for_server_i.clear()
        output_file.close()
    
    return

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

main();
#test();

