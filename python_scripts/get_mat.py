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
        #rs_ratio8,add_to_my_list9,email10,print11,export_easylib12
        list = [int(fields[2]),int(fields[3]),int(fields[4]),int(fields[5]),int(fields[6]),int(fields[8]),int(fields[9]),int(fields[10]),int(fields[11])]
        data['satisx'].append(list)
        data['satist'].append(1)
    for line in unsatisfile:
        fields = line.split(',')
        #search3,retrieval4,retrieval_from_search5,preview6,preview_from_search7,
        #rs_ratio8,add_to_my_list9,email10,print11,export_easylib12
        list = [int(fields[2]),int(fields[3]),int(fields[4]),int(fields[5]),int(fields[6]),int(fields[8]),int(fields[9]),int(fields[10]),int(fields[11])]
        data['unsatisx'].append(list)
        data['unsatist'].append(-1)
    pdb.set_trace()
    savemat('two_day.mat', data)
    return

main()
