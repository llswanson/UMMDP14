import sys,os
import pdb

def main():
    originfile = open('satis2014-10-23_22-00-48.log', 'rU')
    originfile2 = open('satis2014-11-12_00-47-14.log', 'rU')
    filelist = ['date']
    output = open(filelist[len(filelist)-1], 'w+')
    for line in originfile:
        fields = line.split(',')
        month = fields[1][:7]
        #pdb.set_trace()
        if month not in filelist[len(filelist)-1]:
            output.close()
            filelist.append(month)
            output = open('satis/satis_'+month, 'w+')
        output.write(line)
    originfile.close()
    for line in originfile2:
        fields = line.split(',')
        month = fields[1][:7]
        #pdb.set_trace()
        if month not in filelist[len(filelist)-1]:
            output.close()
            filelist.append(month)
            output = open('satis/satis_'+month, 'w+')
        output.write(line)
    originfile2.close()
    output.close()
    return
main()
