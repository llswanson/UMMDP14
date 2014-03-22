UMMDP14
=======

Currently Major scripts are in python_script folder

To use the script to generate the output, log on the EC2 box,
go to the script directory /home/ec2-user/UMMDP14/python_scripts.
We have two script right now, apache_parse and app_server_parse.
Both these files now could access all logfiles and generate output
without using any other shell scripts. But you still need to redirect
the output to a directory you would like to store the output.

Updated: We merge and migrate our python scripts to apache.py

E.g.
Step to run the script for apache logs

cd /home/ec2-user/UMMDP14/python_scripts
The first command line input parameter is the server size, and the following are the year you would like the script to run against

E.g 
python apache_ratio_parse.py 15 2013 2014> output/apache_full.out

