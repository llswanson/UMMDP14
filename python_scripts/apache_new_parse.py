import sys
import csv
import re
import os

fields_name = ["client_ip", "timestamp", "http_first_line", "http_status", "response_size",
                             "referrer_url", "user_agent", "time_respond"]

header = ["Date, ", "Expand_Button_Click(E), ", "Research_Topic_Show(R), ", "Search_Count(S), ",
       "R/S, ", "E/R"]

expand_count = 0
rs_show_count = 0
search_count = 0

def load_sections(filename):
    region_file = open(filename, 'r')

    for line in region_file:
        line = line.strip()
        fields = re.split("[\s]+", line)
        http_first_line = fields[5] + " " + fields[6] + " " + fields[7]
        referrer_url = fields[10]
	get_expand_time(http_first_line)
	get_index_time(http_first_line)
        get_search_time(referrer_url, http_first_line)

    region_file.close()
    return

def load_a_day(file_list):
    for file in file_list:
    	if (os.path.exists(file)):
	    load_sections(file)
    return

# list dictionary in list mode
def print_dict_list_mode(my_dict):
    for field in fields_name:
        print field, ": " ,my_dict[field]
    return

# Time that research topic expanded
def get_expand_time(url):
    global expand_count
    search_url = "logevent?eventName=expandspdocframe"
    if url.find(search_url) != -1:
        expand_count += 1
    return

# Time that research topic exist for a search
def get_index_time(url):
    global rs_show_count
    search_url = "index.html?mylist="
    if url.find(search_url) != -1:
       rs_show_count += 1
    return


# Time that a search is conducted
def get_search_time(referrer_url, http_first_line):
    global search_count
    search_url1 = "/do/search?"
    search_url2 = "POST"
    search_url3 = "capload1.umi.com"
    if http_first_line.find(search_url1) != -1 and http_first_line.find(search_url2) != -1 and referrer_url.find(search_url3) == -1:
        search_count += 1
    return

def print_result(year, month, date):
    global expand_count
    global search_count
    global rs_show_count
    '''
    num1 = get_expand_time(fields_dict)
    num2 = get_index_time(fields_dict)
    num3 = get_search_time(fields_dict)
    ''' 
    print year+"-"+month+"-"+date+", "+str(expand_count)+", "+str(rs_show_count)+", "+str(search_count)+", "+"%.3f"%((rs_show_count+0.0)/search_count)+", "+"%.3f"%((expand_count+0.0)/rs_show_count)
    expand_count = 0
    search_count = 0
    rs_show_count = 0
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
                
                load_a_day(file_list)
                print_result(year, month, date)

    

main();
