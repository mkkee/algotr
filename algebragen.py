from tfunc import *;
from random import *;
from anytree import Node, RenderTree;
from tfdb import *;
#import csv;

#e = "r=TF_low(3)+TF_high(3)";
#r = 0;
#
#TF_low(5);

#exec(e);
#print(r);

def TF_getArgumentValue(p):
#	seed();
	param = "";
	v = 0;
	for i in TF_argument_types:
		if i[0] == p:
			param = i;
			break;
	#print(param);
	param_type = param[1];
	param_min = param[2];
	param_max = param[3];
	
	if param_type == 'int':	
		v = randrange(param_min, param_max + 1);
	
	return v;
	
	
def TF_genFunctionStatement():
	params = [];
#	seed();
	f = choice(TF_functionList);
	f_name = f[0];
	f_param_num = f[1];
	#print(f_name, f_param_num, f);
	f_statement = f_name + "(";
	#do all params for the func
	comma = '';
	for i in range(f_param_num):
		f_statement = f_statement + comma + str(TF_getArgumentValue(f[i+2]));
		comma = ',';		
	f_statement = f_statement + ")";
	return f_statement;

def TF_genEquationElement():
	#decide if this is function or number
	if randrange(0, 101) <= TF_functionToNumberPercentage:
		#function
		return TF_genFunctionStatement();
	else:
		return str(randrange(TF_number_min, TF_number_max+1));
		#number

def TF_genEquationOperator():
	return TF_operators[randrange(0, len(TF_operators))];

def TF_genEquationAlgTree(iterations=0):
	o = Node(TF_genEquationOperator());	
	l = Node(TF_genEquationElement());
	r = Node(TF_genEquationElement());
	t = o;	
	t.children = [l, r];
	#randomize number of iterations
	iter = randrange(iterations);
	for i in range(iter):
		o = Node(TF_genEquationOperator());	
		l = Node(TF_genEquationElement());
		r = Node(TF_genEquationElement());
		#move descendants that are leafs to table for randomization
		d = [];
		for desc in t.descendants:
			if desc.is_leaf:
				d.append(desc);
		#choose randomly which descendant to modify
		n = d[randrange(len(d))];
		#print(t.descendants);
		n.name = o.name;
		n.children = [l, r];
	return t;

def TF_getTreeAsString(t):
	s = "";	
	c = t.children;
	if c[0].is_leaf:
		s += '('+c[0].name#+c[0].parent.name;
	else:
		#1==1;
		s += '('+TF_getTreeAsString(c[0]);
	
	s += c[0].parent.name;
	
	if c[1].is_leaf:
		s += c[1].name+')' #+ c[1].parent.name;
	else:
		#1==1;
		s += TF_getTreeAsString(c[1]) + ')';
		
	return s;

	
##############################################################################################################	
seed();
print("Started");
print("We have", len(TF_functionList), "functions availiable to work with");
print("Now loading DB");
TF_DBLoad();
print("We have ", len(TF_DB), "records");	

#equationAlgTreeLeft = TF_genEquationAlgTree(20);
#equationAlgTreeRight = TF_genEquationAlgTree(20);
#equationLogTreeRoot = Node("<");
#equationLogTreeRoot.children = [equationAlgTreeLeft, equationAlgTreeRight]

#for pre, fill, node in RenderTree(equationLogTreeRoot):
#	print("%s%s" % (pre, node.name))

#print starting to generate equations
x=0
while True:
	x += 1;
	#gen one equation
	equationAlgTreeLeft = TF_genEquationAlgTree(20);
	equationAlgTreeRight = TF_genEquationAlgTree(20);
	equationLogTreeRoot = Node("<");
	equationLogTreeRoot.children = [equationAlgTreeLeft, equationAlgTreeRight]
	if x%1000 == 0: 
		print("Testing generated equation #", x);
	TF_DB_OLD = TF_DB;
	true_count = 0
	false_count = 0;
	t_str = TF_getTreeAsString(equationLogTreeRoot);	
	r=0;
	size = len(TF_DB) - TF_argument_types[0][3] - TF_argument_types[1][3];
	for i in range(size):
		r=0;
		t_exec = "r="+t_str;
		try:
			exec(t_exec);
		except:
			1==1;
			break;
		#print(r);
		if r:
			true_count += 1;
		else:
			false_count += 1;
		TF_DB = TF_DB[1::];
	#print("restoring DB");
	TF_DB = TF_DB_OLD;
	if true_count>0 and false_count>0:
		print("True count =", true_count, "False count =", false_count);	
		print(t_str);
		for pre, fill, node in RenderTree(equationLogTreeRoot):
			print("%s%s" % (pre, node.name))

	
#for pre, fill, node in RenderTree(equationLogTreeRoot):
#	print("%s%s" % (pre, node.name))

	
print("End");
exit(0);


