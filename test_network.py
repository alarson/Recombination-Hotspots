#This file tests a network. Pass in initial configurations, see the results.
#mostly a sanity check
from scipy import *
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import model
import sys
import pickle
import model
from scipy import stats
max_cycle=20
attractor_sets = [[ [-1,1,-1,1,-1,1,-1,1,-1,1],
						[1,1,-1,1,-1,1,-1,1,-1,1],
						[-1,-1,-1,1,-1,1,-1,1,-1,1],
						[-1,1,1,1,-1,1,-1,1,-1,1],
						[-1,1,-1,-1,-1,1,-1,1,-1,1],
						[-1,1,-1,1,1,1,-1,1,-1,1],
						[-1,1,-1,1,-1,-1,-1,1,-1,1],
						[-1,1,-1,1,-1,1,1,1,-1,1],
						[-1,1,-1,1,-1,1,-1,-1,-1,1],
						[-1,1,-1,1,-1,1,-1,1,1,1],
						[-1,1,-1,1,-1,1,-1,1,-1,-1]
						],
					  [[-1,1,-1,1,-1,-1,1,-1,1,-1],
					  [1,1,-1,1,-1,-1,1,-1,1,-1],
					  [-1,-1,-1,1,-1,-1,1,-1,1,-1],
					  [-1,1,1,1,-1,-1,1,-1,1,-1],
					  [-1,1,-1,-1,-1,-1,1,-1,1,-1],
					  [-1,1,-1,1,1,-1,1,-1,1,-1],
					  [-1,1,-1,1,-1,1,1,-1,1,-1],
					  [-1,1,-1,1,-1,-1,-1,-1,1,-1],
					  [-1,1,-1,1,-1,-1,1,1,1,-1],
					  [-1,1,-1,1,-1,-1,1,-1,-1,-1],
					  [-1,1,-1,1,-1,-1,1,-1,1,1]
					  ]]

def get_top_performers(cutoff,population,phase):
	'''
	phase can be 1 (part A) or 2 (part B)
	'''
	fitnesses = [model.GRN.evaluate_network(individual, max_cycle, phase ,attractor_sets) for individual in population]
	percentile95=np.percentile(fitnesses, cutoff)
	top_performers = [individual for individual in population if individual.fitness>=percentile95]

	# top_fitnesses = [ind.fitness for ind in top_performers]
	# # fit = stats.norm.pdf(top_fitnesses, np.mean(top_fitnesses), np.std(top_fitnesses))  #this is a fitting indeed

	# # plt.plot(sorted(top_fitnesses),fit,'-o')

	# plt.hist(top_fitnesses,normed=True)      #use this to draw histogram of your data

	plt.show() 

	print "number of top performers: "+str(len(top_performers))
	print "avg fitness for percentile: "+str(np.mean([i.fitness for i in top_performers]))
	print "avg mod for percentile: "+str(np.mean([i.measure_modularity() for i in top_performers]))

	return top_performers


def main(v):
	# v = v[1:]
	# for el in range(10):
	# 	v[el] = int(v[el])

	# nodes = np.array(v)
	# max_cycle=20
	
	# with open('best_network.pickle', 'rb') as handle:
 #  		individual = pickle.load(handle)

	# print "the network:" 
	# print individual.edges

	
 #  	individual.nodes=nodes
 #  	print individual.nodes
 #  	individual.visualize_network()
	# counter = 0
	# while(counter <= max_cycle and individual.update_state()):
	# 	counter += 1
	# 	print individual.nodes
	# 	individual.visualize_network()

	# if(counter <= max_cycle):
	# 	print "stable"
	# 	print individual.nodes
	# else:
	# 	print "chaotic or cyclic"

	# individual.visualize_network()

	exp1 = "E4"
	exp2 = "E5"
	percentile = 75
	trial_1_populationsA = []
	trial_1_populationsB = []
	trial_2_populationsA = []
	trial_2_populationsB = []
	
	with open('networks/'+exp1+'/run2/populationsA.pickle', 'rb') as handle:
  		for pop in pickle.load(handle):
  			trial_1_populationsA+=pop
  		print len(trial_1_populationsA)
  	# with open('networks/'+exp1+'/populationsA.pickle', 'rb') as handle:
  	# 	trial_1_populationsA+=(pickle.load(handle))[0]
  	# 	print "\n"
  	# 	print len(trial_1_populationsA)
  	with open('networks/'+exp1+'/run2/populationsB.pickle', 'rb') as handle:
  		for pop in pickle.load(handle):
  			trial_1_populationsB+=pop
  	# with open('networks/'+exp1+'/populationsB.pickle', 'rb') as handle:
  	# 	trial_1_populationsB+=(pickle.load(handle))[0]

  	with open('networks/'+exp2+'/run2/populationsA.pickle', 'rb') as handle:
  		for pop in pickle.load(handle):
  			trial_2_populationsA+=pop
  	# with open('networks/'+exp2+'/populationsB.pickle', 'rb') as handle:
  	# 	trial_2_populationsA+=(pickle.load(handle))[0]

  	with open('networks/'+exp2+'/run2/populationsB.pickle', 'rb') as handle:
  		for pop in pickle.load(handle):
  			trial_2_populationsB+=pop
  	# with open('networks/'+exp2+'/populationsB.pickle', 'rb') as handle:
  	# 	trial_2_populationsB+=(pickle.load(handle))[0]

  	print len(trial_1_populationsA)
  	print len(trial_1_populationsB)
  	print len(trial_2_populationsA)
  	print len(trial_2_populationsB)
  	
	
	#trim population down to unique geneological trees? difficult when crossing over (multiple networks with same age)
	print "\n"+exp1+" part A"
	trial_1_top_performersA = get_top_performers(percentile,trial_1_populationsA,1)
	print "\n"+exp1+" part B"
	trial_1_top_performersB = get_top_performers(percentile,trial_1_populationsB,2)

	print "\n"+exp2+" part A"
	trial_2_top_performersA = get_top_performers(percentile,trial_2_populationsA,1)
	print "\n"+exp2+" part B"
	trial_2_top_performersB = get_top_performers(percentile,trial_2_populationsB,2)
	

	#t-test
	print "\nt value for comparing modularity, part A"
	t, p = stats.ttest_ind([i.measure_modularity() for i in trial_1_top_performersA],[i.measure_modularity() for i in trial_2_top_performersA])
	print "ttest_ind: t = %g  p = %g" % (t, p)
	print "t value for comparing modularity, part B"
	t, p = stats.ttest_ind([i.measure_modularity() for i in trial_1_top_performersB],[i.measure_modularity() for i in trial_2_top_performersB])
	print "ttest_ind: t = %g  p = %g" % (t, p)

	print "t value for comparing fitness, part A"
	t, p = stats.ttest_ind([i.fitness for i in trial_1_top_performersA],[i.fitness for i in trial_2_top_performersA])
	print "ttest_ind: t = %g  p = %g" % (t, p)
	print "t value for comparing fitness, part B"
	t, p = stats.ttest_ind([i.fitness for i in trial_1_top_performersB],[i.fitness for i in trial_2_top_performersB])
	print "ttest_ind: t = %g  p = %g" % (t, p)

	print "\nt value for comparing modularity between parts A and B in "+exp1
	t, p = stats.ttest_ind([i.measure_modularity() for i in trial_1_top_performersA],[i.measure_modularity() for i in trial_1_top_performersB])
	print "ttest_ind: t = %g  p = %g" % (t, p)

	print "\nt value for comparing modularity between parts A and B in "+exp2
	t, p = stats.ttest_ind([i.measure_modularity() for i in trial_2_top_performersA],[i.measure_modularity() for i in trial_2_top_performersB])
	print "ttest_ind: t = %g  p = %g" % (t, p)


  	individual=trial_1_top_performersA[0]
	target_stateA = np.array([-1,1,-1,1,-1,1,-1,1,-1,1])
	individual.rectangle_visualization(attractor_sets[0],target_stateA, "TargetA")

	for start_state in attractor_sets[0]:
  		individual.visualize_network(start_state,target_state,max_cycle)
  		temp = raw_input("enter to end")
main(sys.argv)