#!/bin/bash
dir1='/home/ec2-user/ummdp/logfiles/101/apache_access/2013'
dir2='/home/ec2-user/ummdp/logfiles/102/apache_access/2013'
dir3='/home/ec2-user/ummdp/logfiles/103/apache_access/2013'
dir='/home/dianazh/mdp/logfiles/UMMDP14/logfiles'
appname='elibdmz-elibweb_usage.log.2013-'
servername='elibrary.bigchalk.com-access_log.13'
month=0
end='*'
app=''
serv=''
appout='result/app_out_2013_'
servout='result/serv_out_2013_'
cd $dir
for ((i=0;i<12;i++)) do
    month=$(($i+1))
#app=$appname$(printf '%02d' $month)$end
#python app_server_parse.py $dir1$app $dir2$app $dir3$app > $appout$(printf '%02d' $month)
    serv=$servername$(printf '%02d' $month)$end
    python apache_parse.py $dir1$serv $dir2$serv $dir3$serv > $servout$(printf '%02d' $month)
#echo $app
#echo $serv
done
