import sys
import csv
import re
import os

fields_name = ["client_ip", "timestamp", "http_first_line", "http_status", "response_size",
                             "referrer_url", "user_agent", "time_respond"]

header = ["Date, ", "Expand_Button_Click(E), ", "Research_Topic_Show(R), ", "Search_Count(S), ",
       "R/S, ", "E/R"]

file_size = 0
fields_dict = dict()

def load_sections(filename):
    region_file = open(filename, 'r')

    for line in region_file:
        line = line.strip()
        fields = re.split("[\s]+", line)
        '''fields_dict["client_ip"].append(fields[0]) 
        fields_dict["timestamp"].append(fields[3])'''
        fields_dict["http_first_line"].append(fields[5] + " " + fields[6] + " " + fields[7])
        '''fields_dict["http_status"].append(fields[8])
        fields_dict["response_size"].append(fields[9])'''
        fields_dict['referrer_url'].append(fields[10])
    region_file.close()
    return

def load_a_day(filename1,filename2,filename3):
    index = 0
    for x in fields_name:
        fields_dict[fields_name[index]] = []
        index += 1
    load_sections(filename1)
    load_sections(filename2)
    load_sections(filename3)
    return

# list dictionary in list mode
def print_dict_list_mode(my_dict):
    for field in fields_name:
        print field, ": " ,my_dict[field]
    return

# Time that research topic expanded
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

# Time that research topic exist for a search
def get_index_time(my_dict):
    #urls = my_dict["referrer_url"]
    urls = my_dict["http_first_line"]
    count = 0
    for url in urls:
        search_url = "index.html?mylist="
        if url.find(search_url) != -1:
            count += 1
        else:
            continue
    return count

'''
def get_search_time(my_dict):
    urls = my_dict["referrer_url"]
    count = 0
    for url in urls:
        search_url = "/do/results?"
        if url.find(search_url) != -1:
            count += 1
        else: 
            continue
    return count
'''

# Time that a search is conducted
def get_search_time(my_dict):
    refs = my_dict["referrer_url"]
    urls = my_dict["http_first_line"]
    count = 0
    '''
    for url in urls:
        search_url = "/do/results?set=search"
        search_tag = "start=1"

        if url.find(search_url) != -1 and url.find(search_tag) != -1:
            count += 1
        else: 
            continue'''
    #for url in urls:
    for i in range (0,len(urls)):
        search_url1 = "/do/search?"
	search_url2 = "POST"
	search_url3 = "capload1.umi.com"
        if urls[i].find(search_url1) != -1 and urls[i].find(search_url2) != -1 and refs[i].find(search_url3) == -1:
            count += 1
    return count

def print_expand_result(year, month, date):
    num1 = get_expand_time(fields_dict)
    num2 = get_index_time(fields_dict)
    num3 = get_search_time(fields_dict) 
    print year+"-"+month+"-"+date+", "+str(num1)+", "+str(num2)+", "+str(num3)+", "+"%.3f"%((num2+0.0)/num3)+", "+"%.3f"%((num1+0.0)/num2)
    return

def main():
    header_str = ""
    for item in header:
        header_str += item
    print header_str

    dir1 = '/home/ec2-user/ummdp/logfiles/101/apache_access/2013/'
    dir2 = '/home/ec2-user/ummdp/logfiles/102/apache_access/2013/'
    dir3 = '/home/ec2-user/ummdp/logfiles/103/apache_access/2013/'
    dir4 = '/home/ec2-user/ummdp/logfiles/101/apache_access/2014/'
    dir5 = '/home/ec2-user/ummdp/logfiles/102/apache_access/2014/'
    dir6 = '/home/ec2-user/ummdp/logfiles/103/apache_access/2014/'
    '''
    dirh1 = '/home/dianazh/mdp/UMMDP14/2014_web/101/'
    dirh2 = '/home/dianazh/mdp/UMMDP14/2014_web/102/'
    dirh3 = '/home/dianazh/mdp/UMMDP14/2014_web/103/'
    '''
    file13 = 'elibrary.bigchalk.com-access_log.13'
    file14 = 'elibrary.bigchalk.com-access_log.14'
    
    for x in range(1,13):
        month = "%02d" %(x)
        for y in range (1,32):
                date = "%02d" %(y)
                file1 = dir1+file13+month+date
                file2 = dir2+file13+month+date
                file3 = dir3+file13+month+date
                '''
                file4 = dirh1+file14+month+date
                file5 = dirh2+file14+month+date
                file6 = dirh3+file14+month+date
                '''
                if (os.path.exists(file1) and os.path.exists(file2) and os.path.exists(file3)):
                        load_a_day(file1,file2,file3)
                        print_expand_result('13',month,date)
    

    for x in range(1,13):
        month = "%02d" %(x)
        for y in range (1,32):   
                date = "%02d" %(y)
                file1 = dir4+file14+month+date
                file2 = dir5+file14+month+date
                file3 = dir6+file14+month+date
                '''
                file4 = dirh1+file14+month+date
                file5 = dirh2+file14+month+date
                file6 = dirh3+file14+month+date
                '''
                if (os.path.exists(file1) and os.path.exists(file2) and os.path.exists(file3)):
                        load_a_day(file1,file2,file3)
                        print_expand_result('14',month,date)
    return

main();
