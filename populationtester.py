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
	
##############################################################################################################	
start_time = timer()
seed();

print("Started");
print('Argument List:', str(sys.argv))

print("Now loading DB");
tfdb.TF_DBLoad();
data_size = len(tfdb.__TF_DB__);
print("Data size = ", data_size);
print("Load population");

file_name = sys.argv[2];
periods_to_keep = int(sys.argv[1]);
pop_table = [];
importer = JsonImporter();
error_cnt=0;

#file format is: ("True count | False count | Found # | Equation # | Found Pct | Json");	
with open(file_name, newline='') as csvfile:
	filereader = csv.reader(csvfile, delimiter = '|');
	#filereader.__next__(); #skip first line, or add to skip N first lines
	for row in filereader:
		try:
			data_true_count  = row[0];
			data_false_count = row[1];
			data_json = row[5];
			#convert equation to tree
			t = importer.import_(data_json);
			#print(data_json);
			#print(TF_getTreeAsString(t));
			db_row = [int(data_true_count), int(data_false_count), data_json, TF_getTreeAsString(t)];
			pop_table.append(db_row);
			#print(db_row);
			#__TF_DB__.append(db_row);
		except: #skipping wrong rows
			1==1;
			error_cnt = error_cnt + 1;
			#print("Error");
			continue;

print("Loaded population data. Count =", len(pop_table), "Errors=", error_cnt);


TF_DB_OLD = tfdb.__TF_DB__;
size = len(tfdb.__TF_DB__) - TF_argument_types[0][3] - TF_argument_types[1][3] - periods_to_keep;

tfdb.__TF_DB__ = tfdb.__TF_DB__[periods_to_keep::];

#testing population
#trans_end_idx = 0;
#trade_count = 0;

db_trade_index = 0; #index to move along DB copy to calc trade results
pop_result_table = []; #main table for results

#populate result table
for z in range(len(pop_table)):
	pop_result_table.append([0, 0, 0, 0, ""]); # result | trans cnt | positive_trans_cnt | positive_trans_pct | transaction map
	
i=0;
p=0;


for i in range(size): #for each row in data DB
	p=0;
	for p in range(len(pop_table)): #for each population entry
		r=0;
		t_exec = "r="+pop_table[p][3];
		pop_switch = True; #decide on which result we have a signal
		if pop_table[p][0]> pop_table[p][1]: 
			pop_switch = False;
		try:
			exec(t_exec);
		except:
			1==1;
			print("Exception");
			break;
		if (pop_switch and r) or (not pop_switch and not r): #we have transaction here
			trade_start_price = tfdb.__TF_DB__[0][3]; #hard index as we are going to down the table
			trade_end_price = TF_DB_OLD[db_trade_index][3];
			buy_result = trade_end_price - trade_start_price;
			pop_result_table[p][0] = pop_result_table[p][0] + buy_result;
			pop_result_table[p][1] = pop_result_table[p][1] + 1;
			if buy_result > 0:
				pop_result_table[p][2] = pop_result_table[p][2] + 1; #summing all positive transactions
			pop_result_table[p][4] = pop_result_table[p][4] + "1"; #transaction map
		else:#to handle transact string when no transaction
			pop_result_table[p][4] = pop_result_table[p][4] + "0";
			###############  add info about profitable transactions, min and max prfit and lost
	tfdb.__TF_DB__ = tfdb.__TF_DB__[1::];
	db_trade_index = db_trade_index + 1;
	

max_result = 0;
max_result_per_trans = 0;

print("############################################################### DATA TO FOLLOW ########################################");	

print("Result | Result per Trans | Trans Cnt | Signal Type | Strategy Type | Positive Trans Cnt | Positive Trans Pct | Eq in Str | JSON | Transaction Map");
for i in range(len(pop_result_table)):
	#just to find some max values for bottom statisitcs
	if abs(pop_result_table[i][0]) > abs(max_result): 
		max_result = pop_result_table[i][0];
	if abs(pop_result_table[i][0]/pop_result_table[i][1]) > abs(max_result_per_trans): 
		max_result_per_trans = pop_result_table[i][0]/pop_result_table[i][1];
	if int(pop_table[i][0]) < int(pop_table[i][1]):
		data_signal_type = True;
	else:
		data_signal_type = False;
	if float(pop_result_table[i][0]) < 0:
		data_strategy_type = 'SELL'; 
	else:
		data_strategy_type = 'BUY'; 
	
	if pop_result_table[i][0] < 0: #flip positive transaction count if result is negative
		pop_result_table[i][2] = pop_result_table[i][1] - pop_result_table[i][2];
	
	pop_result_table[i][3] = pop_result_table[i][2]/pop_result_table[i][1]; #pct of positive transactions
	
	print("{0:.4f}".format(pop_result_table[i][0])+"|"+"{0:.4f}".format(pop_result_table[i][0]/pop_result_table[i][1])+"|"+str(pop_result_table[i][1])+"|"+str(data_signal_type)
	      +"|"+data_strategy_type+"|"+str(pop_result_table[i][2])+"|"+"{0:.4f}".format(pop_result_table[i][3])+"|"+pop_table[i][3]+"|"+pop_table[i][2]+"|"+pop_result_table[i][4]);
	
print("############################################################### DATA END ##############################################");	

print("Max Result = ", max_result);
print("Max Result per # trans = ", max_result_per_trans);
	
#print("restoring DB");
tfdb.__TF_DB__ = TF_DB_OLD;

print("End");
end_time = timer();
print("Elapsed Time: ", end_time - start_time);

exit(0);