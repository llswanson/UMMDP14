import sys
import csv
import os
import collections

def load_counts_per_session():
    session_dist_search = dict()
    session_dist_preview = dict()
    session_dist_retrieval = dict()

    rs_ratio_dict = dict()
    for i in range (-1, 21):
        rs_ratio_dict[i] = 0
    print rs_ratio_dict;

    dir_root = '/home/ec2-user/UMMDP14/app_server_parsed/' 
    file_list = os.listdir(dir_root)
    for filename in file_list:
        the_file = open(dir_root + filename, 'rU')
        is_first_line = True
        for line in the_file:
            if is_first_line:
                is_first_line = False
                continue
            else:
                fields = line.split(',')
                # should be session_id, date, search#, retrieval#, retrival from search#, preview#, preview from search#, rs_ratio#
                search_count = int(fields[2]) 
                retrieval_count = int(fields[3])
                preview_count = int(fields[5])
                rs_ratio = float(fields[7])
                     
                if search_count not in session_dist_search:
                    session_dist_search[search_count] = 1
                else: 
                    session_dist_search[search_count] += 1

                if retrieval_count not in session_dist_retrieval:
                    session_dist_retrieval[retrieval_count] = 1
                else:
                    session_dist_retrieval[retrieval_count] += 1

                if preview_count not in session_dist_preview:
                    session_dist_preview[preview_count] = 1
                else:
                    session_dist_preview[preview_count] += 1

                if rs_ratio < 0:
                    rs_ratio_dict[-1] += 1
                elif (int(rs_ratio) > 20):
                    rs_ratio_dict[20] += 1
                else:
                    rs_ratio_dict[int(rs_ratio)] += 1
                   

    # order dicts
    ordered_session_dist_search = collections.OrderedDict(sorted(session_dist_search.items()))
    ordered_session_dist_retrieval = collections.OrderedDict(sorted(session_dist_retrieval.items()))
    ordered_session_dist_preview = collections.OrderedDict(sorted(session_dist_preview.items()))
    ordered_rs_ratio = collections.OrderedDict(sorted(rs_ratio_dict.items()))
    
    output_root = '/home/ec2-user/UMMDP14/session_distribution/' 
    output_1 = open(output_root + 'SD_search', 'w+')
    output_1.write('# of search,# of session,\n')
    for k, v in ordered_session_dist_search.iteritems():
        output_1.write( str(k) + ',' + str(v) + ',\n')
    output_1.close()
    output_2 = open(output_root + 'SD_retrieval', 'w+')
    output_2.write('# of retrieval,# of session,\n')
    for k, v in ordered_session_dist_retrieval.iteritems():
        output_2.write( str(k) + ',' + str(v) + ',\n')
    output_2.close()
    output_3 = open(output_root + 'SD_preview', 'w+')
    output_3.write('# of preview,# of session,\n')
    for k, v in ordered_session_dist_preview.iteritems():
        output_3.write( str(k) + ',' + str(v) + ',\n') 
    output_3.close()

    output_4 = open(output_root + 'SD_rs_ratio', 'w+')
    output_4.write('bucket, ratio\n')
    for k, v in ordered_rs_ratio.iteritems():
        output_4.write( str(k) + ',' + str(v) + ',\n')
    output_4.close()

    return

load_counts_per_session();
