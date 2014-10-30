import os, sys
import pdb
import time

def main():
    #path = '/home/ec2-user/UMMDP14/app_server_parsed'
    path = '/home/ec2-user/UMMDP14/app_sp_test/'
    dirs = os.listdir(path)
    dirs.sort()
    output = open('unsatis'+time.strftime('%Y-%m-%d_%H-%M-%S')+'.log', 'w+')
    for filename in dirs:
        first_line = True
        file = open(path + filename, 'rU')
        for line in file:
            fields = line.split(',')
            if first_line:
                first_line = False
                continue
            #filter out entries that has no searches
            elif int(fields[2]) == 0:
                continue
            else:
                #filter out users that has more search than retrieval
                if float(fields[7]) < 1 and float(fields[8]) ==0 and float(fields[9]) == 0 and float(fields[10]) == 0 and float(fields[11]) == 0:
                    output.write(line)
        file.close()
    output.close() 
    return

main()
