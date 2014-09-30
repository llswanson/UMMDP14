import pygal 
import sys
import csv
import re
import os

session_table = dict()

avg_search_per_session = []
avg_retrieval_per_session = []
avg_preview_per_session = []
session_count_per_day = []
date_list = []

def load_session_table():
	file_list = os.listdir('/Users/hongbo/Desktop/test_log')

	for f in file_list:
		region_file = open('/Users/hongbo/Desktop/test_log/' + f, 'rU')
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
				search_count += int(fields[1])
				retrieval_count += int(fields[2])
				preview_count += int(fields[3])
				plot_date = fields[4]
				
		avg_search_per_session.append(search_count / session_count)
		avg_retrieval_per_session.append(retrieval_count / session_count)
		avg_preview_per_session.append(preview_count / session_count)
		session_count_per_day.append(session_count)
		date_list.append(plot_date)

load_session_table();

def plot_line_chart():
	line_chart = pygal.Line()
	line_chart.title = 'Proquest Search Usability Test'
	line_chart.x_labels = date_list
	line_chart.add('Average search per session', avg_search_per_session)
	line_chart.add('Average retrieval per session', avg_retrieval_per_session)
	line_chart.add('Average preview per session', avg_preview_per_session)
	line_chart.add('Session amonut', session_count_per_day)
	line_chart.render_to_file('bar_chart.svg')

def main():
	plot_line_chart()

main()


