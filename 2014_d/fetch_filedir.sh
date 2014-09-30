#! /bin/bash
for i in {101..115};
do
    find /home/ec2-user/ummdp/logfiles/$i -name elibdmz\* | sort > app_server$i
done
