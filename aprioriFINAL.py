##################################################################
#   CS 378 Data Mining                                            #
#   Shuoyuan (Steve) Yang, Joseph Lee                             #
#   Feb 17th 2017                                                 #
#                                                                 #
################################################################## 


import sys
import time
import itertools
from collections import *


data = sys.argv[1]
min_sup_count = int(sys.argv[2])
outputName = sys.argv[3]



count2 = {}    ## count2 stores C2



lines = []


##################################################################
#   takes in the dataset                                          #
#   go through line by line and seperate them into                #
#   one List of List and store as dataset                         #
#                                                                 #
################################################################## 

with open(data) as file:
    for line in file.readlines():
        line = [int(each) for each in line.split()]
        lines.append(line)

dataset = lines

##################################################################
# Input:                                                          #
#      1: Dataset of transaction                                  #
#	   2: Threshold (minimum support count)                       #
# Output:                                                         #
#      Final result of frequent L2 item set as well as generating #
#      C1                                                         #
#                                                                 #
# function:                                                       #
#      Takes in the transaction dataset, go through the dataset   #
#      and then Generate C1, as well as generating C2.            #
#      After generating C2, it will prune out those do not        #
#      meet the minium threshold, and then store the final result #
#      of L2 into a global variable "count2", and then return C1  #
#                                                                 #
################################################################## 
   
def one_item_count_and_generateL2(transaction, support):   ####DONE also will count 2
	
	C1 = {}
	
	for row in transaction:
		for item in row:
			if item in C1:
				C1[item] += 1
			else:
				C1[item] = 1
			for item2 in row:
				if item < item2:
					s = (item, item2)
					if s in count2:
						count2[s] += 1
					else:
						count2[s] = 1

	removeCount2 = {k for k in count2 if count2[k] < support}

	for k in removeCount2: 
		del count2[k]


	return C1

##################################################################
# Input:                                                          #
#      1: Dataset of transaction                                  #
#	   2: Threshold (minimum support count)                       #
# Output:                                                         #
#      Final result of frequent SINGLE item set L1                #
#                                                                 #
# function:                                                       #
#      Takes in the transaction dataset, and call another         #
#      to count the occurance of frequent SINGLE item             #
#                                                                 #
################################################################## 

def frequent_single_and_two_item(transaction, support):   

	'transaction is data'

	L1 = one_item_count_and_generateL2(transaction, support)
	
	toBeRemovedList = {k for k in L1 if L1[k] < support}

	for k in toBeRemovedList: 
		del L1[k]


	return L1

##################################################################
# Input:                                                          #
#      1. frequency set of Lk-1                                   #
#      2. K                                                       #
# Output:                                                         #
#      Return a list of candidate Ck                              #
#                                                                 #
################################################################## 

def generate_candidate(Lkminus1, k):

	candidateK = []

	
	for item1 in Lkminus1:
		for item2 in Lkminus1:
			check = True
			if item1 != item2:
				lst_item1 = list(item1)
				lst_item2 = list(item2)

				for i in range(k-2):
					check = check and (lst_item1[i]==lst_item2[i])
				if check == True and lst_item1[k-2]<lst_item2[k-2]:
					lst_item1.append(lst_item2[k-2])
					union = set(lst_item1)
					candidateK.append(union)
					

	return candidateK


##################################################################
# Input:                                                          #
#      1: Dataset of transaction                                  #
#	   3: a list of candidate without count                       #
#      2: Threshold (minimum support count)                       #  
# Output:                                                         #
#      Return a dictionary of Lk with count                       #
#                                                                 #
# function:                                                       #
#      Calculate the frequency of each group of item,             #
#      prune out the items that do not meet the support count     #
################################################################## 

def count_frequency(transaction, c_wo_count, support_count):     #### scanning the database, and then generate Ck

	c_with_count = {}

	for tran in transaction:
		for elem in c_wo_count:


			if elem.issubset(tran):
				
				tmp = tuple(elem)
				if tmp in c_with_count:

					c_with_count[tmp]+=1

				else:
					
					c_with_count[tmp] = 1


	toBeRemovedList = {k for k in c_with_count if c_with_count[k] < support_count}

	for k in toBeRemovedList: 
		del c_with_count[k]

			

	return c_with_count

##################################################################
# Input:                                                          #
#      1: Dataset of transaction                                  #
#	   2: Threshold (minimum support count)                       #
# Output:                                                         #
#      Final result of the frequent purchase items                #
#                                                                 #
# function:                                                       #
#      Serves as a "main" function of the program                 #
################################################################## 


def apriori(dataset, minimum_support_count):

	toBeReturned = []     ## this is the final list that would be appended, sorted, and then printed


	L1 = frequent_single_and_two_item(dataset, minimum_support_count)
	
	toBeReturned.append(L1)           ## append L1 into the toBeRetunred list

	L2 = count2                       ##count 2 is frequent-2-item set, and now pass it into L2

	toBeReturned.append(L2)

	Lk = L2             

	k = 3

	while Lk:

		Lklist = sorted(Lk.keys())    ## Since Lk is a dictionary, which is not sorted. Lklist is a sorted list of Lk of WITHOUT the count.
		Ck = generate_candidate(Lklist, k)       
		Lk = count_frequency(dataset, Ck, minimum_support_count)
		
		toBeReturned.append(Lk)

		k=k+1

	return toBeReturned






t0 = time.time()	
a = apriori(dataset, min_sup_count)
t1 = time.time()

fw = open(outputName,"w")

for tran in a:	
	for each in tran:
		count = tran[each]
		if type(each) == tuple:
			
			each = ' '.join(map(str, each))

			
			
			fw.write(str(each)+"  (%s)\n"%str(count))
		else:
			
			fw.write(str(each)+" (%s)\n"%str(count))
fw.close()



print( 'time elapsed:    ',t1-t0 )





