import sys
import csv
import re
import os

#fields_name = ["client_ip", "timestamp", "http_first_line", "http_status", "response_size",
#                             "referrer_url", "user_agent", "time_respond"]

header = ["Date, ", "Expand_Button_Click, ", "Research_Topic_Show, ", "Search_Count, ", "R/E"]

file_size = 0
fields_dict = dict()

def load_sections(filename):
    region_file = open(filename, 'r')

    for line in region_file:
        line = line.strip()
        fields = re.split("[\s]+", line)
        fields_dict["http_first_line"].append(fields[5] + " " + fields[6] + " " + fields[7])
        fields_dict['referrer_url'].append(fields[10])
    region_file.close()
    return

def load_a_day(file_list):
    index = 0    

    for file in file_list:
    	for x in fields_name:
      	fields_dict[fields_name[index]] = []
      	index += 1
    	if (os.path.exists(file)):
	    load_sections(file)
    return
    #load_sections(filename1)
    #load_sections(filename2)
    #load_sections(filename3)
    #return

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

def get_index_time(my_dict):
    urls = my_dict["referrer_url"]
    count = 0
    for url in urls:
        search_url = "index.html?mylist="
        if url.find(search_url) != -1:
            count += 1
        else:
            continue
    return count

def get_search_time(my_dict):
    urls = my_dict["referrer_url"]
    count = 0
    for url in urls:
        search_url = "/do/results?set=search"
        search_tag = "start=1"

        if url.find(search_url) != -1 and url.find(search_tag) != -1:
            count += 1
        else: 
            continue
    return count

def print_expand_result(year, month, date):
    num1 = get_expand_time(fields_dict)
    num2 = get_index_time(fields_dict)
    num3 = get_search_time(fields_dict) 
    print year+"-"+month+"-"+date+", "+str(num1)+", "+str(num2)+", "+str(num3)+", "+str((num2+0.0)/num3)
    return

def main():

    header_str = ""
    for item in header:
        header_str += item
    print header_str

    server_num = int(sys.argv[1])
    server_names = []
    for i in range (0, server_num):
        my_server = 101 + i
        server_names.append(str(my_server))

    log_years = []
    for year in range(2, len(sys.argv)):
	log_years.append(sys.argv[year])

    file_prefix = 'elibrary.bigchalk.com-access_log.'
    dir_prefix = '/home/ec2-user/ummdp/logfiles/'
    directories = dict()

    for year in log_years:
        directories[year] = []
    	for it in server_names:
	    single_dir_name = dir_prefix + it + "/apache_access/" + year + "/"
	    directories[year].append(single_dir_name)

    for year in log_years:
    	for x in range(1,13):
            month = "%02d" %(x)
            for y in range (1,32):
                date = "%02d" %(y)
		file_list = []
		for i in range (0, server_num):
		    file_list.append(directories[year][i] + file_prefix + year[2:] + month + date)
		    print (directories[year][i] + file_prefix + year[2:] + month + date)
                
                load_a_day(file_list)
                print_expand_result(year, month, date)

    
'''
    for x in range(1,13):
        month = "%02d" %(x)
        for y in range (1,32):   
                date = "%02d" %(y)
		
                file1 = dir4+file14+month+date
                file2 = dir5+file14+month+date
                file3 = dir6+file14+month+date

                        load_a_day(file1,file2,file3)
                        print_expand_result('14',month,date)
    return
'''

main();
