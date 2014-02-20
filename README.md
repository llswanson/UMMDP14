UMMDP14
=======

Currently Major scripts are in python_script folder

To use the script to generate the output, log on the EC2 box,
go to the script directory /home/ec2-user/UMMDP14/python_scripts.
We have two script right now, appache_parse and app_server_parse.
Both these files now could access all logfiles and generate output
without using any other shell scripts. But you still need to redirect
the output to a directory you would like to store the output.

E.g.
Step to run the script for app_server

cd /home/ec2-user/UMMDP14/python_scripts
python app_server_parse.py > output/app_server_output1
