cd /home/ec2-user/proquest/logfiles/log101
gunzip *.gz
python /home/ec2-user/UMMDP14/app_server_parse.py elibdmz-elibweb_usage.log.* > server101.out
gzip elibdmz*
cd /home/ec2-user/proquest/logfiles/log102
gunzip *.gz
python /home/ec2-user/UMMDP14/app_server_parse.py elibdmz-elibweb_usage.log.* > server102.out
gzip elibdmz*
cd /home/ec2-user/proquest/logfiles/log103
gunzip *.gz
python /home/ec2-user/UMMDP14/app_server_parse.py elibdmz-elibweb_usage.log.* > server103.out
gzip elibdmz*

