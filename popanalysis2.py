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

	
#lets build best set of equations for each starting population
############## what to build
### main loop to go through NEW SETS of populations - while not found
### comparing if it is possible to add a population without overlap - adding to NEW SETS 1
### if not added then this set is only added to final resullt
### if added then the set stays and we continute till end of population loop then
### then again through what is left in SETS table untill nothing can be added

### populate population sets with single item sets equal to population list
pop_sets = []; #initial sets
pop_sets_1 = []; #workign version to handle loop correctly
pop_sets_result = []; #this will be final size of population sets

#populate initial sets table with single sets
for i in pop_table:
	pop_sets.append([i]);

print(len(pop_sets));	
pop_sets[0].append(pop_table[4]);	
print(len(pop_sets));	
pop_sets.append([pop_table[7]]);	
print(len(pop_sets));	
	
print("Loaded sets table");
print(pop_table[0]);
print(pop_sets[0]);

added = True;
while added:
	added = False;
	#for each in sets
	for s in pop_sets:
		#for each in pop 
		for p in pop_table:
			# try to add pop to a set
			#check if overlap exists with any pop in a set
			for sp in s:
				num_trans = sum(analyzed_eq_map);
				overlap_trans = [a and b for a,b in zip(analyzed_eq_map,row_eq_map)]# analyzed_eq_map and row_eq_map;
				overlap_pct = sum(overlap_trans) / num_trans;
				row_eq_map = pop_trans_map_table[k];
	# if added add new set to sets
	# if nothing added add the set to results
	#copy to new sets
	
#copy all form sets to results
	
exit()

print("############################################################### DATA TO FOLLOW ########################################");	
#print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
#pop_to_keep_table.sort(key=lambda x: abs(x[1]), reverse=True);
for i in range(len(pop_table)):
	print("##################### Analyzing strategy #:", i+1);
	print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
	print(str(pop_table[i][0])+"|"+str("{0:f}".format(pop_table[i][1]))+"|"+str(pop_table[i][2])+"|"+str(pop_table[i][3])+"|"+str(pop_table[i][4])+"|"+str(pop_table[i][5])+"|"+str("{0:f}".format(pop_table[i][6]))+"|"+pop_table[i][7]+"|"+pop_table[i][8]+"|"+pop_table[i][9])
	###############Add all eq that has less than X overlaping transactions. 
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

exit();

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