import sys,os
import pdb

def main(files):
    for filename in files[1:]:
        originfile = open(filename, 'rU')
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
        output.close()
    return

main(sys.argv)
