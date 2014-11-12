import os, sys
import pdb
import time

def get_by_date():
    path = '/home/ec2-user/UMMDP14/app_server_parsed/'
    #path = '/home/ec2-user/UMMDP14/app_sp_test/'
    dirs = os.listdir(path)
    dirs.sort()
    for filename in dirs:
        file = open(path + filename, 'rU')
        output = open('unsatis_date/unsatis_' + filename, 'w+')
        for line in file:
            fields = line.split(',')
            if len(fields) < 2:
                print filename + line
                continue
            #filter out entries that has no searches
            if 'search' in fields[2]:
                continue
            if int(fields[2]) == 0:
                continue
            else:
                #filter out users that has more search than retrieval
                if float(fields[7]) < 1 and float(fields[8]) ==0 and float(fields[9]) == 0 and float(fields[10]) == 0 and float(fields[11]) == 0:
                    output.write(line)
        output.close() 
        file.close()
    return

def get_by_month():
    path = '/home/ec2-user/UMMDP14/python_scripts/unsatis_date/' 
    dirs = os.listdir(path)
    dirs.sort()
    filelist = ['null']
    output = open('unsatis/unsatis_' + filelist[len(filelist)-1], 'a')
    for filename in dirs:
        if not filename[8:] in filelist[len(filelist)-1]:
            output.close()
            filelist.append(filename[8:-3])
            #pdb.set_trace()
            output = open('unsatis/unsatis_' + filelist[len(filelist)-1], 'a')
        file = open(path + filename, 'rU')
        output.write(file.read())

def main():
    get_by_date()
    get_by_month()
   
main() 
