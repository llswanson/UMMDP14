import pygal 
import sys
import csv
import re
import os

session_table = dict()

month_table = {'01': 'January', '02': 'February', '03' : 'March', '04' : 'April', '05' : 'May',
			   '06': 'June', '07': 'July', '08' : 'Augest', '09' : 'September', '10': 'October',
			   '11': 'November', '12': 'December'}

def load_session_table_monthly(path):
	search_amount = []
	retrieval_amount = []
	preview_amount = []
	session_count_per_day = []
	date_list = []

	file_list = os.listdir(path)

	for f in file_list:
		if f[0] == '.':
			continue

		region_file = open(path + f, 'rU')
		first_line = True

		session_count = 0
		search_count = 0
		retrieval_count = 0
		preview_count = 0
		plot_date = '2000-01-01'

		for line in region_file:
			if first_line == True:
				first_line = False 
				continue
			else:
				#operation  
				fields = line.split(",")
				session_count += 1
				search_count += int(fields[2])
				retrieval_count += int(fields[3])
				preview_count += int(fields[4])
				#plot_date = fields[1]
				date_fileds = fields[1].split("-")
				plot_date = date_fileds[2]
				
		search_amount.append(search_count / (session_count * 1.0) )
		retrieval_amount.append(retrieval_count / (session_count * 1.0) )
		preview_amount.append(preview_count / (session_count * 1.0) )
		session_count_per_day.append(session_count)
		date_list.append(plot_date)

	#print search_amount
	res = [search_amount, retrieval_amount, preview_amount, session_count_per_day, date_list]
	return res


def plot_line_chart(year, month, info):
	
	search_amount = info[0]
	retrieval_amount = info[1]
	preview_amount = info[2]
	session_count_per_day = info[3]
	date_list = info[4]
	line_chart = pygal.Line()
	stackedline_chart = pygal.StackedLine(fill=True)
	line_chart.title = 'Proquest Search Usability Test for ' + year + " " + month_table[month]
	line_chart.x_labels = date_list
	line_chart.add('Search/Session', search_amount)
	line_chart.add('Retrival/Session', retrieval_amount)
	line_chart.add('Preview/Session', preview_amount)
	#line_chart.add('Session amonut', session_count_per_day)

	line_chart.render_to_file('/Users/hongbo/Desktop/visualization/bar_chart' + year + '-' + month + '.svg')


def plot_line_chart_sum(search_sum, retrieval_sum, preview_sum, monthes):
	
	line_chart = pygal.Line()
	stackedline_chart = pygal.StackedLine(fill=True)
	line_chart.title = 'Proquest Search Usability Test from 2013' 
	line_chart.x_labels = monthes
	line_chart.add('Search/Session', search_sum)
	line_chart.add('Retrival/Session', retrieval_sum)
	line_chart.add('Preview/Session', preview_sum)
	#line_chart.add('Session amonut', session_count_per_day)

	line_chart.render_to_file('/Users/hongbo/Desktop/visualization/bar_chart_total.svg')


def main():
	plot_monthly()
	#print search_sum
	

def plot_monthly():
	path_prefix = "/Users/hongbo/Downloads/app_server_parsed_grouped/files_"
	month_total = []
	search_sum = []
	retrieval_sum = []
	preview_sum = []
	session_sum = []

	month_2013 = []
	month_2014 = []
	for i in range(1, 13):
		if i < 10:
			month_2013.append('0' + str(i))
		else:
			month_2013.append(str(i))
	for i in range(1, 9):
		month_2014.append('0' + str(i))

	for i in range(0, 12):
		path = path_prefix + '2013-' + month_2013[i] + '/'
		info = load_session_table_monthly(path);
		month_total.append('13' + month_2013[i])

		field_sum = 0.0
		for j in info[0]:
			field_sum += j
		search_sum.append(field_sum / (1.0 * len(info[0])))

		field_sum = 0.0
		for j in info[1]:
			field_sum += j
		retrieval_sum.append(field_sum / (1.0 * len(info[0])))

		field_sum = 0.0
		for j in info[2]:
			field_sum += j
		preview_sum.append(field_sum / (1.0 * len(info[0])))

		plot_line_chart('2013', month_2013[i], info)

	for i in range(0, 8):
		path = path_prefix + '2014-' + month_2014[i] + '/'
		#print path
		month_total.append('14' + month_2014[i])
		info = load_session_table_monthly(path);

		field_sum = 0.0
		for j in info[0]:
			field_sum += j
		search_sum.append(field_sum / (1.0 * len(info[0])))

		field_sum = 0.0
		for j in info[1]:
			field_sum += j
		retrieval_sum.append(field_sum / (1.0 * len(info[0])))

		field_sum = 0.0
		for j in info[2]:
			field_sum += j
		preview_sum.append(field_sum / (1.0 * len(info[0])))		

		plot_line_chart('2014', month_2014[i], info)

	plot_line_chart_sum(search_sum, retrieval_sum, preview_sum, month_total)

main()




