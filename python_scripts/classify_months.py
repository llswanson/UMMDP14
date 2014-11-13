import threading 

from svmclassify import classify_month

def main():
    t1 = threading.Thread(name='2013-10', target=classify_month, args=('2013-10',))
    t2 = threading.Thread(name='2013-09', target=classify_month, args=('2013-09',))

    print 'start t1'
    t1.start()
    
    print 'start t2'
    t2.start()
    return

main()
