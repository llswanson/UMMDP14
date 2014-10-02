#! /bin/bash
for i in {1..9};
do
    mkdir /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2013-0$i 
    cp -r $(find /home/ec2-user/UMMDP14/app_server_parsed_grouped/ -name 2013-0$i* | sort) /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2013-0$i
    mkdir /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2014-0$i
    cp -r $(find /home/ec2-user/UMMDP14/app_server_parsed_grouped/ -name 2014-0$i* | sort) /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2014-0$i
done
for i in {10..12};
do
    mkdir /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2013-$i 
    cp -r $(find /home/ec2-user/UMMDP14/app_server_parsed_grouped/ -name 2013-$i* | sort) /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2013-$i
    mkdir /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2014-$i 
    cp -r $(find /home/ec2-user/UMMDP14/app_server_parsed_grouped/ -name 2014-$i* | sort) /home/ec2-user/UMMDP14/app_server_parsed_grouped/files_2014-$i
done
