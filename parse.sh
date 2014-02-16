#!/bin/bash
dir1='/home/ec2-user/ummdp/logfiles/101/apache_access/2014/'
dir2='/home/ec2-user/ummdp/logfiles/102/apache_access/2014/'
dir3='/home/ec2-user/ummdp/logfiles/103/apache_access/2014/'
dir='/home/dianazh/mdp/logfiles/UMMDP14/logfiles'
appname='elibdmz-elibweb_usage.log.2013-'
servername='elibrary.bigchalk.com-access_log.14'
month=0
end='*'
app=''
serv=''
appout='result/app_out_2013_'
servout='result/2014/serv_out_2013_'
#cd $dir
for ((i=0;i<2;i++)) do
    month=$(($i+1))
#app=$appname$(printf '%02d' $month)$end
#python app_server_parse.py $dir1$app $dir2$app $dir3$app > $appout$(printf '%02d' $month)
    serv=$servername$(printf '%02d' $month)$end
    python apache_parse.py $dir1$serv $dir2$serv $dir3$serv > $servout$(printf '%02d' $month)
#echo $app
#echo $serv
done
