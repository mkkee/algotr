import tfdb;
from tfunc import *;
#from tftreegen import *;
from tftreegen import TF_getTreeAsString;

import csv;
from random import *;
from anytree import Node, RenderTree;
from anytree.exporter import JsonExporter;
from anytree.importer import JsonImporter;
from timeit import default_timer as timer
import sys;
from glob import glob;
	
##############################################################################################################	
start_time = timer()
seed();

print("Started");
print('Argument List:', str(sys.argv));

#print("Now loading DB");
#tfdb.TF_DBLoad();
#data_size = len(tfdb.__TF_DB__);
#print("Data size = ", data_size);

print("Load population");
#file_name = sys.argv[2]; ##might need to expand as wildcards are used there
pct_pop_to_keep = int(sys.argv[1]);
print("Percentage to keep =", pct_pop_to_keep);

#file_name = 'poptesting0003.txt';
#pct_pop_to_keep = 1;

pop_table = [];
pop_to_keep_table = [];

importer = JsonImporter();

error_cnt = 0;

file_cnt = 0;

for file_name in glob(sys.argv[2]):
	file_cnt = file_cnt+1;
#	print("Loading data from: ", file_name);
	with open(file_name, newline='') as csvfile:
		filereader = csv.reader(csvfile, delimiter = '|');
		#filereader.__next__(); #skip first line, or add to skip N first lines
		for row in filereader:
			try:
#"Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Eq in Str | JSON");
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
#				if int(data_true_count) < int(data_false_count):
#					data_signal_type = True;
#				else:
#					data_signal_type = False;
#				if float(data_result) < 0: 
#					data_strategy_type = 'SELL'; 
#				else:
#					data_strategy_type = 'BUY'; 
				#t = importer.import_(data_json);
				db_row = [float(data_result), float(data_result_per_trans), int(data_trans_count), data_signal_type, data_strategy_type, int(data_positive_trans_cnt), float(data_positive_trans_pct), data_eq_string, data_json, data_trans_map];
				pop_table.append(db_row);
			except: #skipping wrong rows
				1==1;
				error_cnt = error_cnt + 1;
				#print("Error");
				continue;
	#close(file_name); #check if needed

print("Loaded population data from ", file_cnt, "Count =", len(pop_table), "Errors =", error_cnt);

k = int(len(pop_table)*pct_pop_to_keep/100); #how many rows to keep
################## add dividing k/2 to select 50% of what is needed in each step 
print("Rows to keep =", k);

#sort by result
pop_table.sort(key=lambda x: abs(x[0]), reverse=True);
for i in range(k):
	pop_to_keep_table.append(pop_table[i]);
#	print(pop_table[i][0], "{0:f}".format(pop_table[i][1]), pop_table[i][2], pop_table[i][3]);

#sort by result per trans
pop_table.sort(key=lambda x: abs(x[1]), reverse=True);
for i in range(k):
	pop_to_keep_table.append(pop_table[i]);
#	print(pop_table[i][0], "{0:f}".format(pop_table[i][1]), pop_table[i][2], pop_table[i][3]);


#sort by positive trans pct
pop_table.sort(key=lambda x: abs(x[6]), reverse=True);
for i in range(k):
	pop_to_keep_table.append(pop_table[i]);
#	print(pop_table[i][0], "{0:f}".format(pop_table[i][1]), pop_table[i][2], pop_table[i][3]);


pop_to_keep_table.sort(key=lambda x: (abs(x[1]), x[5]), reverse=True); #sort by result and equation text to eliminate duplicates
pop_to_keep_table_unique = [];
prev_row = [];
for i in range(len(pop_to_keep_table)):
	if prev_row != pop_to_keep_table[i]:
		pop_to_keep_table_unique.append(pop_to_keep_table[i]);
	prev_row = pop_to_keep_table[i];	
	#print(pop_to_keep_table[i][0], "{0:f}".format(pop_to_keep_table[i][1]), pop_to_keep_table[i][2], pop_to_keep_table[i][3], pop_to_keep_table[i][4], pop_to_keep_table[i][5], pop_to_keep_table[i][6]);

print("Selected ", len(pop_to_keep_table_unique), "Unique rows. From ", len(pop_to_keep_table), "selected rows.");

#final sorting order
pop_to_keep_table_unique.sort(key=lambda x: (x[6]), reverse=True); #sort by positive trans pct
	
print("############################################################### DATA TO FOLLOW ########################################");	
print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
#pop_to_keep_table.sort(key=lambda x: abs(x[1]), reverse=True);
for i in range(len(pop_to_keep_table_unique)):
	print(str(pop_to_keep_table_unique[i][0])+"|"+str("{0:f}".format(pop_to_keep_table_unique[i][1]))+"|"+str(pop_to_keep_table_unique[i][2])+"|"+str(pop_to_keep_table_unique[i][3])+"|"+str(pop_to_keep_table_unique[i][4])+"|"+str(pop_to_keep_table_unique[i][5])+"|"+str("{0:f}".format(pop_to_keep_table_unique[i][6]))+"|"+pop_to_keep_table_unique[i][7]+"|"+pop_to_keep_table_unique[i][8]+"|"+pop_to_keep_table_unique[i][9])
	
print("########################################################### DATA END ####################################");

print("End");
end_time = timer();
print("Elapsed Time: ", end_time - start_time);
exit();