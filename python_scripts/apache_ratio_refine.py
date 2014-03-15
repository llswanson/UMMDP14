import sys
import csv
import re
import os

header = ["Date, ", "Expand_Button_Click(E), ", "Research_Topic_Show(R), ", "Search_Count(S), ", "Advance_Search_Count(A), ",
          "Core_Correalation_Click, ", "Exit_Button_Click, ", "Educator_Tool_Click, ","My_List_Click, ","Bookcarts_Click, ","Slideshows_Click, ","Timelines_Click, ","Quizzes_Click, ", "R/S, ", "E/R, ", "A/S"]

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
        get_advance_search_time(http_first_line)
        get_core_corre_time(http_first_line)
        get_exit_click_time(http_first_line)
        get_educator_tool_click_time(http_first_line)
    get_mylist_click(http_first_line)
    get_bookcarts_click(http_first_line)
    get_slideshows_click(http_first_line)
    get_timelines_click(http_first_line)
    get_quizzes_click(http_first_line)

    region_file.close()
    return

def load_a_day(file_list):
    for file in file_list:
        if (os.path.exists(file)):
        load_sections(file)
    return

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
    
    sys.stdout.write(year + "-" + month + "-" + date + ", ")
    sys.stdout.write(str(expand_count) + ", ")
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
    sys.stdout.write("%.3f"%((advance_search_count+0.0)/search_count))
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
