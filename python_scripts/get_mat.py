from scipy.io import savemat
import sys
import csv
import re
import os
import pdb

def main():
    #file = open('satis2014-10-23_22-00-48.log','rU')
    satisfile = open('2day_satis', 'rU')
    unsatisfile = open('2day_unsatis', 'rU')
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
    pdb.set_trace()
    savemat('two_day.mat', data)
    return

main()
