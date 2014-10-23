import sys
import csv
import re
import os
import urllib
import pdb
import time

fields_name = ["timestamps", "program_name", "product_SKU", "request_type", "request_url", "client_ip", "query", "request_service", "resource_type",
               "resource_id", "description", "result_count", "response_code", "response_time", "user_id", "user_account", "group_account",
               "library_card", "referer_url", "thread_id", "session_id", "search_id", "request_id", "content_length", "session_sequence", "grade",
               "user_role", "server", "hostname", "owner_id", "search_mode", "delivery_method", "access_method", "selling_method", "contract_type",
               "delivery_format", "document_source", "dumy1", "content_type", "authentication_method", "language", "interface_type", "dumy2",
               "subscription_id", "usage_type", "user_agent"]
error_msg = open('error'+time.strftime('%Y-%m-%d_%H-%M-%S')+'.log', 'w+')
satis_msg = open('satis'+time.strftime('%Y-%m-%d_%H-%M-%S')+'.log', 'w+')

# generate dict: 
#   session_id : dict of (field_name : list of values)
def load_sections(filename):
  session_dict = dict()
  region_file = open(filename, 'rU')
  index = 0
  
  for line in region_file:
    index = 0
    fields = line.split(";;|")
    if (len(fields) >=5):
        # filter out internal ip
        ip = fields[5]
        if ((not ip) or ip.find("165.215") != -1):
            continue
    else:
        error_msg.write("Error1 No ip field @ " + filename + line + '\n')
        continue

    if (len(fields) >= 20):
        session_id = fields[20]
    else: 
        # session_id may be in url
        query_str = urllib.unquote(fields[6])
        #delete the stirng that might separte a session id
        query_str.replace("\n>","") 
        # Warning: if the arbitrary query string contain ts= 
        # for non-query purpose this might generate error
        ts_start = query_str.find("ts=")
        if (ts_start != -1):
            ts_start += 3
            session_id = query_str[ts_start:ts_start+32]
            formatstr = re.match('([a-fA-F\d]*)',session_id)
            if (formatstr.group() == ''):
                error_msg.write("Error2 no session id @ " + filename + line + '\n')
                continue
        else:
            error_msg.write("Error2 no session id @ " + filename + line + '\n')
            continue
  
    if session_id not in session_dict:
      session_dict[session_id] = dict()

    # add each line of log files into each fields list
    for field in fields:
      if fields_name[index] not in session_dict[session_id]:
        session_dict[session_id][fields_name[index]] = []
      session_dict[session_id][fields_name[index]].append(field)
      index += 1

  region_file.close()
  return session_dict

def load(file):
    session_dict = load_sections(file)
    session_table = dict()
    for session_id in session_dict:
        if session_id not in session_table:
            session_table[session_id] = dict()
        
        if 'request_url' not in session_dict[session_id]:
            error_msg.write('no request_url in session id: ' + session_id+'\n')
            error_msg.write( session_dict[session_id])
            error_msg.write('\n')
            exit(1)
        if 'request_service' not in session_dict[session_id]:
            error_msg.write( 'no request_service in session id: ' + session_id + '\n')
            error_msg.write( session_dict[session_id])
            error_msg.write('\n')
            exit(1)
        if 'query' not in session_dict[session_id]:
            error_msg.write('no query in session id: ' + session_id + '\n') 
            error_msg.write(session_dict[session_id])
            error_msg.write('\n')
            exit(1)
        urls = session_dict[session_id]["request_url"]
        types = session_dict[session_id]["request_service"]
        queries = session_dict[session_id]["query"]
        if (len(urls) != len(types) or len(types) != len(queries)):
            error_msg.write('Error: field length don\' match @ ' + file + ' session: ' + session_id +'\n')
        get_features(session_table[session_id], urls, types, queries)
    return session_table    

def get_features(session_table_perid, urls, types, queries):
    # pdb.set_trace()
    session_table_perid['search'] = get_session_search_counts(urls, types, queries)
    session_table_perid['preview'], session_table_perid['preview_from_search'] = get_session_preview_counts(urls, types, queries) 
    session_table_perid['retrieval'], session_table_perid['retrieval_from_search'] = get_session_retrieval_counts(urls, types, queries)
    session_table_perid['addtomylist'] = get_session_addtomylist_counts(urls, types, queries)
    session_table_perid['email'] = get_session_email_counts(urls, types, queries)
    session_table_perid['print'] = get_session_print_counts(urls,types, queries)
    session_table_perid['export_easylib'] = get_export_easylib_counts(urls, types, queries)
    return

def get_session_search_counts(urls, types, queries):
    search_url1 = "/do/search"
    search_url2 = "SEARCH_SEARCH"
    
    session_search_counts = 0
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_search_counts += 1
    return session_search_counts

def get_session_retrieval_counts(urls, types, queries):
    search_url1 = "/do/document"
    search_url2 = "SEARCH_DOC_RETRIEVAL;;Document"
    search_url3 = "set=search"

    session_retrieval_counts = 0
    session_retrieval_from_search = 0
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_retrieval_counts += 1
        if queries[i].find(search_url3) != -1:
            session_retrieval_from_search += 1
    return session_retrieval_counts, session_retrieval_from_search

def get_session_preview_counts(urls, types, queries):
    search_url1 = "/do/document"
    search_url2 = "SEARCH_DOC_RETRIEVAL;;DocumentPreview"
    search_url3 = "set=search"

    session_preview_counts = 0
    session_preview_from_search = 0
    for i in range (0,len(urls)):
      if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
        session_preview_counts += 1
        if queries[i].find(search_url3) != -1:
            session_preview_from_search += 1
    return session_preview_counts, session_preview_from_search

def get_session_addtomylist_counts(urls, types, queries):
    # count all the files that are added to mylist
    # without specifying if is a regular doc or research topic
    search_url1 = '/do/mylist'
    search_url2 = 'MyListComponent'
    search_url3 = 'mylist=add'

    session_addtomylist_counts = 0
    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1 and queries[i].find(search_url3) != -1:
           session_addtomylist_counts += 1
    return session_addtomylist_counts 
       
def get_session_email_counts(urls, types, queries):
    search_url1 = '/do/email'
    search_url2 = 'set=search'

    session_email_counts = 0
    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and queries[i].find(search_url2) != -1:
           session_email_counts += 1
    return session_email_counts 

def get_session_print_counts(urls, types, queries):
    search_url1 = '/do/document'
    search_url2 = 'set=search'
    search_url3 = 'style=printable'

    session_print_counts = 0
    for i in range (0, len(urls)):
        if urls[i].find(search_url1) != -1 and queries[i].find(search_url2) != -1 and queries[i].find(search_url3) != -1:
           session_print_counts += 1
    return session_print_counts 

def get_export_easylib_counts(urls, types, queries):
    search_url1 = '/do/exportToEasyBib'
    search_url2 = 'ExportToEasyBibComponent;;ExportToEasyBib' 

    session_export_easylib_counts = 0
    for i in range(0, len(urls)):
        if urls[i].find(search_url1) != -1 and types[i].find(search_url2) != -1:
            session_export_easylib_counts += 1
    return session_export_easylib_counts
         
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
    header_str = "session_id,date,search,retrieval,retrieval_from_search,preview,preview_from_search," + \
                        "rs_ratio,add_to_my_list,email,print,export_easylib," 
    satis_msg.write(header_str + newline)
    cont_run = False
    for date in ordered_date:
        # write session table to a file
        write_filename = write_file_prefix + date
        output_file = open(write_filename, 'w+')
        output_file.write(header_str + newline)

        # get session table for a day
        for i in range(101, 116):
            if (date not in app_server[i]['files']):
                error_msg.write('Error: no logfile for date: ' + date + 'on server: ' + str(i) + '\n')
                continue

            if (date == '2014-09-23'):
                cont_run = True
            if (not cont_run):
                continue
 
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
                output_file.write(key + comma + date + comma + str(value['search']) + comma + \
                                str(value['retrieval']) + comma + str(value['retrieval_from_search']) + comma + \
                                str(value['preview']) + comma +str(value["preview_from_search"]) + comma + \
                                str(rs_ratio) + comma + str(value['addtomylist']) + comma + \
                                str(value['email']) + comma + str(value['print']) + comma + \
                                str(value['export_easylib']) + comma + newline)
           
                # for collection purpose
                if (value['addtomylist'] != 0 or value['email'] != 0 or value['print'] != 0 or value['export_easylib'] != 0):
                    satis_msg.write(key + comma + date + comma + str(value['search']) + comma + str(value['retrieval']) + comma + str(value['retrieval_from_search']) + comma + str(value['preview']) + comma +str(value["preview_from_search"]) + comma + str(rs_ratio) + comma + str(value['addtomylist']) + comma + str(value['email']) + comma + str(value['print']) + comma + str(value['export_easylib'])+ comma + newline)
            
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

