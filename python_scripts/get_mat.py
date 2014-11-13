from scipy.io import savemat
import sys
import csv
import re
import os
import pdb

def main():
    satispath = '/home/ec2-user/UMMDP14/python_scripts/satis/' 
    unsatispath = '/home/ec2-user/UMMDP14/python_scripts/unsatis/'
    satislist = os.listdir(satispath)
    unsatislist = os.listdir(unsatispath)
    satislist.sort()
    unsatislist.sort()
    if len(unsatislist) != len(satislist):
        print 'error'
        return
    
    for name in satislist:
        if '2013' not in name and '2014' not in name:
            continue
        month = name[-7:]
        satisfile = open(satispath + 'satis_' + month, 'rU')
        unsatisfile = open(unsatispath + 'unsatis_' + month, 'rU')
        gen_mat_file(month, satisfile, unsatisfile)
        satisfile.close()
        unsatisfile.close()
    return

def gen_mat_file(month_str, satisfile, unsatisfile):
    data = {}
    data['satisx'] = []
    data['satist'] = []
    data['unsatisx'] = []
    data['unsatist'] = []
    for line in satisfile:
        fields = line.split(',')
        #search3,retrieval4,retrieval_from_search5,preview6,preview_from_search7,
        #rs_ratio8,add_to_my_list9,email10,prfloat11,export_easylib12
        list = [float(fields[2]),float(fields[3]),float(fields[4]),float(fields[5]),float(fields[6]),float(fields[8]),float(fields[9]),float(fields[10]),float(fields[11])]
        data['satisx'].append(list)
        data['satist'].append(1.0)
    
    for line in unsatisfile:
        fields = line.split(',')
        #search3,retrieval4,retrieval_from_search5,preview6,preview_from_search7,
        #rs_ratio8,add_to_my_list9,email10,prfloat11,export_easylib12
        list = [float(fields[2]),float(fields[3]),float(fields[4]),float(fields[5]),float(fields[6]),float(fields[8]),float(fields[9]),float(fields[10]),float(fields[11])]
        data['unsatisx'].append(list)
        data['unsatist'].append(-1.0)
    savemat('matfiles/' + month_str + '.mat', data)
    return

main()
