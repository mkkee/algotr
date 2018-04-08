import tfdb;
from tfunc import *;
from tftreegen import *;

from random import *;
from anytree import Node, RenderTree;
from anytree.exporter import JsonExporter;
from timeit import default_timer as timer
import sys;

	
##############################################################################################################	
start_time = timer()
seed();

print("Started");
print('Argument List:', str(sys.argv));
exp_number_to_find = int(sys.argv[1]);
print("Running to find ", exp_number_to_find, "equations");

#exp_number_to_find = 1000;

print("Now loading DB");
tfdb.TF_DBLoad();
data_size = len(tfdb.__TF_DB__);
print("Data size = ", data_size);

signal_desired_max_pct = 0.15;
signal_desired_min_pct = 0.05;
 
#json exporter from anytree
exp = JsonExporter();

exp_found= 0;

x=0
print("########################################################### DATA TO FOLLOW ##############################");
print("True count | False count | Equation # | Found Pct | Json");	

#while True:
while exp_found < exp_number_to_find:
	x += 1;
	#gen one equation
	equationAlgTreeLogical = TF_genEquationAlgTreeLogical(2);     ####################################### MAIN TREE GENERATION LINE
	TF_DB_OLD = tfdb.__TF_DB__;
	true_count = 0
	false_count = 0;
	t_str = TF_getTreeAsString(equationAlgTreeLogical);	
	r=0;
	size = len(tfdb.__TF_DB__) - TF_argument_types[0][3] - TF_argument_types[1][3];
	#failed = False;
	for i in range(size):
		#print(len(__TF_DB__));
		r=0;
		t_exec = "r="+t_str;
		try:
			exec(t_exec);
		except:
			1==1;
			#failed = True;
			break;
		#print(r);
		if r:
			true_count = true_count+1;
		else:
			false_count = false_count+1;
		tfdb.__TF_DB__ = tfdb.__TF_DB__[1::];
	#print("restoring DB");
	tfdb.__TF_DB__ = TF_DB_OLD;
	if true_count>0 and false_count>0 and ((true_count/data_size<signal_desired_max_pct and true_count/data_size>signal_desired_min_pct) or (false_count/data_size>signal_desired_min_pct and false_count/data_size<signal_desired_max_pct)):
		#print(exp.export(equationAlgTreeLogical));
		exp_found = exp_found + 1;
		print(str(true_count)+"|"+str(false_count)+"|"+str(exp_found)+"|"+str(x)+"|"+"{0:f}".format(exp_found/x)+"|"+exp.export(equationAlgTreeLogical));	

print("########################################################### DATA END ####################################");
	
print("End");
end_time = timer();
print("Elapsed Time: ", end_time - start_time);

exit(0);