import tfdb;
from tfunc import *;
from tftreegen import TF_getTreeAsString;

import csv;
from random import *;
from anytree import Node, RenderTree;
from anytree.exporter import JsonExporter;
from anytree.importer import JsonImporter;
from timeit import default_timer as timer
import sys;
from glob import glob;
from statistics import pstdev;
	
##############################################################################################################	
start_time = timer()

print("Started");
print('Argument List:', str(sys.argv));

pop_table = [];
importer = JsonImporter();
error_cnt = 0;
file_cnt = 0;

for file_name in glob(sys.argv[1]):
	file_cnt = file_cnt+1;
#	print("Loading data from: ", file_name);
	with open(file_name, newline='') as csvfile:
		filereader = csv.reader(csvfile, delimiter = '|');
		#filereader.__next__(); #skip first line, or add to skip N first lines
		for row in filereader:
			try:
#"Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct |  Eq in Str | JSON | Transaction Map"
				data_result = row[0];
				data_result_per_trans = float(row[1]);
				data_trans_count = row[2];
				data_signal_type  = row[3];
				data_strategy_type = row[4];
				data_positive_trans_cnt = row[5];
				data_positive_trans_pct = row[6];
				data_eq_string = row[7];
				data_json = row[8];		
				data_trans_map = row[9];		
				db_row = [float(data_result), float(data_result_per_trans), int(data_trans_count), data_signal_type, data_strategy_type, int(data_positive_trans_cnt), float(data_positive_trans_pct), data_eq_string, data_json, data_trans_map];
				pop_table.append(db_row);
			except: #skipping wrong rows
				1==1;
				error_cnt = error_cnt + 1;
				#print("Error");
				continue;
	#close(file_name); #check if needed

print("Loaded population data from ", file_cnt, "Count =", len(pop_table), "Errors =", error_cnt);

print("Preparing for analysis");
print("Static analysis of each equation");
#sort by something
#pop_table.sort(key=lambda x: abs(x[0]), reverse=True);

#loading transaction map for each population as int
pop_trans_map_table = [];

for i in range(len(pop_table)):
	trans_map = pop_table[i][9];
	trans_map_row = [];
	for k in trans_map:
		trans_map_row.append(int(k));
	pop_trans_map_table.append(trans_map_row);

	
#print the map
print();
for i in range(len(pop_trans_map_table)):
		for k in range(len(pop_trans_map_table[i])):
			print(pop_trans_map_table[i][k], end='')
		print();
#	print(str(pop_table[i][0])+"|"+str("{0:f}".format(pop_table[i][1]))+"|"+str(pop_table[i][2])+"|"+str(pop_table[i][3])+"|"+str(pop_table[i][4])+"|"+str(pop_table[i][5])+"|"+str("{0:f}".format(pop_table[i][6]))+"|"+pop_table[i][7]+"|"+pop_table[i][8]+"|"+pop_table[i][9])
print();

#calculate trans freq in periods
cnt_200 = 0;
pop_trans_freq_periods_200 = [];
cnt_100 = 0;
pop_trans_freq_periods_100 = [];
cnt_50 = 0;
pop_trans_freq_periods_50 = [];

pop_trans_freq_conuters = [];

########### modify to single loop
for trans_map in pop_trans_map_table:
	cnt_200 = 0;
	freq_row_200 = [];
	cnt_100 = 0;
	freq_row_100 = [];
	cnt_50 = 0;
	freq_row_50 = [];
	for i in range(len(trans_map)):
		if(trans_map[i] == 1):
			cnt_200 = cnt_200 + 1;
		if i>0 and (i % 200) == 0:
			freq_row_200.append(cnt_200);
			cnt_200 = 0;
		if(trans_map[i] == 1):
			cnt_100 = cnt_100 + 1;
		if i>0 and (i % 100) == 0:
			freq_row_100.append(cnt_100);
			cnt_100 = 0;
		if(trans_map[i] == 1):
			cnt_50 = cnt_50 + 1;
		if i>0 and (i % 50) == 0:
			freq_row_50.append(cnt_50);
			cnt_50 = 0;
	freq_row_50.append(cnt_50); #append last periods
	freq_row_100.append(cnt_100);
	freq_row_200.append(cnt_200);
	pop_trans_freq_periods_50.append(freq_row_50);
	pop_trans_freq_periods_100.append(freq_row_100);
	pop_trans_freq_periods_200.append(freq_row_200);
	#calc counter totals
	cnt_50 = 0;
	cnt_100 = 0;
	cnt_200 = 0;
	for i in freq_row_50:
		if i != 0: 
			cnt_50 = cnt_50 + 1;
	for i in freq_row_100:
		if i != 0: 
			cnt_100 = cnt_100 + 1;
	for i in freq_row_200:
		if i != 0: 
			cnt_200 = cnt_200 + 1;
	pop_trans_freq_conuters.append([cnt_200, cnt_100, cnt_50]);
	
periods_50 = len(pop_trans_freq_periods_50[0]);
periods_100 = len(pop_trans_freq_periods_100[0]);
periods_200 = len(pop_trans_freq_periods_200[0]);

pop_to_keep_table = [];
period_200_pct_to_keep = 0.8; #remove all equations that will have frequency on the 200 periods less than this pct

print("############################################################### DATA TO FOLLOW ########################################");	
#print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
#pop_to_keep_table.sort(key=lambda x: abs(x[1]), reverse=True);
for i in range(len(pop_table)):
	print("##################### Analyzing strategy #:", i+1);
	print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
	print(str(pop_table[i][0])+"|"+str("{0:f}".format(pop_table[i][1]))+"|"+str(pop_table[i][2])+"|"+str(pop_table[i][3])+"|"+str(pop_table[i][4])+"|"+str(pop_table[i][5])+"|"+str("{0:f}".format(pop_table[i][6]))+"|"+pop_table[i][7]+"|"+pop_table[i][8]+"|"+pop_table[i][9])
	print("\tSome analized data goes here");
	print("\tPeriod = 200", pop_trans_freq_periods_200[i]);
	print("\tPeriod = 100 ", pop_trans_freq_periods_100[i]);
	print("\tPeriod = 50 ", pop_trans_freq_periods_50[i]);
	print("Standard dev: {0:.2f} {1:.2f} {2:.2f}".format(pstdev(pop_trans_freq_periods_50[i]), pstdev(pop_trans_freq_periods_100[i]), pstdev(pop_trans_freq_periods_200[i])));
	print("Periods fill rate", str("{0:.2f}".format(pop_trans_freq_conuters[i][0]/periods_200*100))+"%", str("{0:.2f}".format(pop_trans_freq_conuters[i][1]/periods_100*100))+"%", str("{0:.2f}".format(pop_trans_freq_conuters[i][2]/periods_50*100))+"%");
	###############add analysis for best not related equations loop through rest of eq to find the best ones
	pop_related = [];
	analyzed_eq_map = pop_trans_map_table[i];
	overlap_trans = 0
	row_eq_map = [];
	num_trans = 0;
	overlap_pct = 0;
	for k in range(i, len(pop_table)): #looping through rest of eqations adding trans overlap pct
		row = [];
		row = pop_table[k];
		row_eq_map = pop_trans_map_table[k];
		num_trans = sum(analyzed_eq_map);
		overlap_trans = [a and b for a,b in zip(analyzed_eq_map,row_eq_map)]# analyzed_eq_map and row_eq_map;
		overlap_pct = sum(overlap_trans) / num_trans;
		row.append(overlap_pct) #adding overlap pct at the end
		pop_related.append(row);
	
	#sort by least related
	pop_related.sort(key=lambda x: (-x[10], abs(x[1])), reverse=True)
	
	end = min(6, len(pop_related));
	#print first 5 least dependant
	print("Overlap Pct | Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
	for k in range(end):
		print("Overlap {0:.4f}% ".format(pop_related[k][10]), end = '');
		print(str(pop_related[k][0])+"|"+str("{0:f}".format(pop_related[k][1]))+"|"+str(pop_related[k][2])+"|"+str(pop_related[k][3])+"|"+str(pop_related[k][4])+"|"+str(pop_related[k][5])+"|"+str("{0:f}".format(pop_related[k][6]))+"|"+pop_related[k][7]+"|"+pop_related[k][8]+"|"+pop_related[k][9])
		
	print(); #empty line to separate eq
#	exit();
print("########################################################### DATA END ####################################");
print();

pop_to_keep_table_1 = [];
stddev_max_value = 10;
#copy the eq that we want to keep based on freq and stddev
for i in range(len(pop_table)):
	if pop_trans_freq_conuters[i][0]/periods_200 >= period_200_pct_to_keep and pstdev(pop_trans_freq_periods_50[i]) <= stddev_max_value:
		pop_to_keep_table_1.append(pop_table[i]);
pop_to_keep_table = pop_to_keep_table_1;

#removal of the same map equations
#sort by result by trans, eq lenght
pop_to_keep_table.sort(key=lambda x: (abs(x[0]), abs(x[1]), -len(x[7])), reverse=True);
pop_to_keep_table_1 = [];
pop_to_keep_table_1.append(pop_to_keep_table[0]);
last_row = pop_to_keep_table[0];
for i in range(len(pop_to_keep_table)):
	#condition when we add
	if pop_to_keep_table[i][1] != last_row[1]:
		#here we add because result is different
		pop_to_keep_table_1.append(pop_to_keep_table[i]);
		last_row = pop_to_keep_table[i];
	elif pop_to_keep_table[i][9] != last_row[9]:
		#adding because map is different
		pop_to_keep_table_1.append(pop_to_keep_table[i]);
		last_row = pop_to_keep_table[i];

pop_to_keep_table = pop_to_keep_table_1;

pop_to_keep_table.sort(key=lambda x: abs(x[1]), reverse=True);	
print("Started with ", len(pop_table), "equations. Only keeping ", len(pop_to_keep_table));
print("############################################################### DATA TO FOLLOW ########################################");	
print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");

for i in range(len(pop_to_keep_table)):
	print(str(pop_to_keep_table[i][0])+"|"+str("{0:f}".format(pop_to_keep_table[i][1]))+"|"+str(pop_to_keep_table[i][2])+"|"+str(pop_to_keep_table[i][3])+"|"+str(pop_to_keep_table[i][4])+"|"+str(pop_to_keep_table[i][5])+"|"+str("{0:f}".format(pop_to_keep_table[i][6]))+"|"+pop_to_keep_table[i][7]+"|"+pop_to_keep_table[i][8]+"|"+pop_to_keep_table[i][9])

print("############################################################### DATA END ##############################################");

print("End");
end_time = timer();
print("Elapsed Time: ", end_time - start_time);
exit();