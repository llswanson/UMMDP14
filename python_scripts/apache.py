import sys
import csv
import re
import os

header = ["Date, ", "Expand_Button_Click(E), ", "Research_Topic_Show(R), ", "Search_Count(S), ", "Advance_Search_Count(A), ",
          "Core_Correalation_Click, ", "Exit_Button_Click, ", "Educator_Tool_Click, ","My_List_Click, ","Bookcarts_Click, ","Slideshows_Click, ","Timelines_Click, ","Quizzes_Click, ", "R/S, ", "E/R, ", "A/S"]

header2 = ["Date, ", "Search from Popular Search, ", "Popular Search from Homepage"]

header3 = ["Data, ", "Search from Specific Time Period, ", "Tag Search"]

expand_count = 0
rs_show_count = 0
search_count = 0
advance_search_count = 0
core_correlation_click_count = 0
exit_click_count = 0
educator_tool_click_count = 0
mylist_count = 0
bookcarts_count = 0
slideshows_count = 0
timelines_count = 0
quizzes_count = 0

popsearch = 0
pophomesearch = 0

searchSTP = 0
tagsearch = 0
def parse_file(filename):
    region_file = open(filename, 'r')
    #i = 0  #test
    for line in region_file:
        #sys.stdout.write("line: "+str(i)+'\n')  #test
        #i += 1  #test
        line = line.strip()
        fields = re.split("[\s]+", line)
        http_first_line = fields[5] + " " + fields[6] + " " + fields[7]
        referrer_url = fields[10]
        '''get_expand_time(http_first_line)
        get_index_time(http_first_line)
        get_search_time(referrer_url, http_first_line)
        get_advance_search_time(http_first_line)
        get_core_corre_time(http_first_line)
        get_exit_click_time(http_first_line)
        get_educator_tool_click_time(http_first_line)
        get_mylist_click(http_first_line)
        get_bookcarts_click(http_first_line)
        get_slideshows_click(http_first_line)
        get_timelines_click(http_first_line)
        get_quizzes_click(http_first_line)
        get_pop_search(http_first_line, referrer_url)'''
        get_search_STP(http_first_line)
        get_tag_search(http_first_line)

    region_file.close()
    return

def load_a_day(file_list):
    exist = False
    #i = 0
    for filename in file_list:
        if (os.path.exists(filename)):
            #sys.stdout.write("server: "+str(i)+'\n')  #test
            #i += 1
            exist = True
            parse_file(filename)
            length = len(filename)
        else:
            exist = exist or False
    if (exist):
        print_result(filename[length-6:length-4],filename[length-4:length-2],filename[length-2:])

# Count that research topic expanded
def get_expand_time(url):
    global expand_count
    search_url = "logevent?eventName=expandspdocframe"
    if url.find(search_url) != -1:
        expand_count += 1
    return

# Count that research topic exist for a search
def get_index_time(url):
    global rs_show_count
    search_url = "index.html?mylist="
    if url.find(search_url) != -1:
       rs_show_count += 1
    return

# Count that a search is conducted
def get_search_time(referrer_url, http_first_line):
    global search_count
    search_url1 = "/do/search?"
    search_url2 = "POST"
    search_url3 = "capload1.umi.com"
    if http_first_line.find(search_url1) != -1 and http_first_line.find(search_url2) != -1 and referrer_url.find(search_url3) == -1:
        search_count += 1
    return

# Count that a advance search is conducted
def get_advance_search_time(url):
    global advance_search_count
    search_url1 = "/do/search?"
    search_url2 = "secondaryNav=advance"
    if url.find(search_url1) != -1 and url.find(search_url2) != -1:
        advance_search_count += 1
    return

# Count core correlation click times
def get_core_corre_time(url):
    global core_correlation_click_count
    search_url = "/teacherweb/elib/do/standards" 
    if url.find(search_url) != -1:
        core_correlation_click_count += 1
    return

# Count exit button (top right corner) click times
def get_exit_click_time(url):
    global exit_click_count
    search_url = "/do/logoff?" 
    if url.find(search_url) != -1:
        exit_click_count += 1
    return

# Count Educator tool click time 
def get_educator_tool_click_time(url):
    global educator_tool_click_count
    search_url = "/do/educatorstool?"
    if url.find(search_url) != -1:
        educator_tool_click_count += 1
    return

# Count My List click time
def get_mylist_click(url):
    global mylist_count
    search_url = "/do/results?"
    search_url2 = "set=mylist"
    if url.find(search_url) != -1 and url.find(search_url2) != -1:
        mylist_count += 1
    return

# Count Bookcarts click time
def get_bookcarts_click(url):
    global bookcarts_count
    search_url = "/do/results?"
    search_url2 = "set=bookcartlist"
    if url.find(search_url) != -1 and url.find(search_url2) != -1:
        bookcarts_count += 1
    return

# Count Slideshows click time
def get_slideshows_click(url):
    global slideshows_count
    search_url = "/do/slideshows?"
    if url.find(search_url) != -1:
        slideshows_count += 1
    return

# Count Timelines click time
def get_timelines_click(url):
    global timelines_count
    search_url = "/do/timelines?"
    if url.find(search_url) != -1:
        timelines_count += 1
    return

# Count Quizzes click time
def get_quizzes_click(url):
    global quizzes_count 
    search_url = "/do/quiz?"
    if url.find(search_url) != -1:
        quizzes_count += 1
    return

def get_pop_search(http_first_line, referrer_url):
    global popsearch
    global pophomesearch
    search_url1 = "/do/search?doasearch=true&reissuesearch=true"
    search_url2 = "/do/search?edition="
    if http_first_line.find(search_url1) != -1:
        popsearch += 1
        if referrer_url.find(search_url2) != -1:
            pophomesearch += 1
    return

def get_search_STP(http_first_line):
    global searchSTP
    search_url = "datetype=between"
    if http_first_line.find(search_url) != -1:
        searchSTP += 1
    return

def get_tag_search(http_first_line):
    global tagsearch
    search_url = "&secondaryNav=tag"
    if http_first_line.find(search_url) != -1:
        tagsearch += 1
    return

#print result and clear globals
def print_result(year, month, date):
    global expand_count
    global search_count
    global rs_show_count
    global advance_search_count
    global core_correlation_click_count
    global exit_click_count
    global educator_tool_click_count
    global mylist_count
    global bookcarts_count
    global slideshows_count
    global timelines_count
    global quizzes_count
    global popsearch
    global pophomesearch
    global searchSTP
    global tagsearch


    sys.stdout.write(year + "-" + month + "-" + date + ", ")
    '''sys.stdout.write(str(expand_count) + ", ")
    sys.stdout.write(str(rs_show_count) + ", ")
    sys.stdout.write(str(search_count) + ", ")
    sys.stdout.write(str(advance_search_count) + ", ")
    sys.stdout.write(str(core_correlation_click_count) + ", ")
    sys.stdout.write(str(exit_click_count) + ", ")
    sys.stdout.write(str(educator_tool_click_count) + ", ")
    sys.stdout.write(str(mylist_count) + ", ")
    sys.stdout.write(str(bookcarts_count) + ", ")
    sys.stdout.write(str(slideshows_count) + ", ")
    sys.stdout.write(str(timelines_count) + ", ")
    sys.stdout.write(str(quizzes_count) + ", ")
    sys.stdout.write("%.3f"%((rs_show_count+0.0)/search_count) + ", ")
    sys.stdout.write("%.3f"%((expand_count+0.0)/rs_show_count) + ", ")
    sys.stdout.write("%.3f"%((advance_search_count+0.0)/search_count+", "))
    sys.stdout.write(str(popsearch)+", ")
    sys.stdout.write(str(pophomesearch)+", ")'''
    sys.stdout.write(str(searchSTP)+", ")
    sys.stdout.write(str(tagsearch))
    sys.stdout.write("\n")

    expand_count = 0
    search_count = 0
    rs_show_count = 0
    advance_search_count = 0
    core_correlation_click_count = 0
    exit_click_count = 0
    educator_tool_click_count = 0
    mylist_count = 0
    bookcarts_count = 0
    slideshows_count = 0
    timelines_count = 0
    quizzes_count = 0

    popsearch = 0
    pophomesearch = 0

    searchSTP = 0
    tagsearch = 0

    return

'''def is_leap_year(year):
    if((year % 4) == 0):
        if((year % 100) == 0):
            if((year % 400) == 0):
                return 1
            else:
                return 0
        else:
         return 1
    return 0'''


def main():

    header_str = ""
    #for item in header:
    #for item in header2:
    for item in header3: 
        header_str += item
    print header_str

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
        for x in range(1,13):
        #for x in range(3,13):
            month = "%02d" %(x)
            for y in range (1,32):
            #for y in range (13, 32):
                date = "%02d" %(y)
                #generate list of file dir for each day(one for each server)
                file_list = []
                for i in range (0, server_num):
                    file_list.append(year_servers[year][i] + file_prefix + year[2:] + month + date)
                load_a_day(file_list)

main();
