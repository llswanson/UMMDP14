import sys,os
import pdb

def main():
    originfile = open('satis2014-10-23_22-00-48.log', 'rU')
    output = open('satis_2day', 'w+')
    i = 0
    for line in originfile:
        fields = line.split(',')
        #pdb.set_trace()
        if fields[1] != '2013-01-01' and fields[1] != '2013-01-02':
            continue
        output.write(line)
    output.close()
    return
main()
