#CMPUT 366 P1 Q1
#Greg Knoblauch
#Bryce Cartman

import blackjack
from pylab import *
import numpy

# GREEDY: Checks the Q values given actions = {hit,stay},
# used for blackjack.printPolicy()
def myGreedyPolicy(state):
	return argmax(Q[state])

# Determines which policy to use (RANDOM or GREEDY) from Emu and Epi
def actionProb(e,a,s):
	numActions = 3
	if np.argmax(Q[s]) == a:
		return 1 - e + (e/numActions)
	else:
		return e/numActions


#Initialize 
Q= 0.00001*rand(181,2)
returnSum = 0.0

numEpisodes = 1000000
alpha = 0.001
Emu = 0.1
Epi = 0.01

# Runs ExpectedSarsa, updating the Q array
for episodeNum in range(numEpisodes):
	#Being blackjack at start state
	state = blackjack.init()
	G = 0
	
	while state != -1:
		#Chooses an action
		action = np.random.choice([0,1], p=[actionProb(Emu, 0, state), actionProb(Emu,1,state)])
		
		#Samples a hand
		reward, nextState = blackjack.sample(state,action)
		
		#Updates Q arrays
		if nextState != -1: 
			Q[state][action] = Q[state][action] + alpha*(reward + ((actionProb(Epi,0,nextState)*Q[nextState][0]) + (actionProb(Epi,1,nextState)*Q[nextState][1])) - Q[state][action])
		else:
			Q[state][action] = Q[state][action] + alpha*(reward - Q[state][action])
			
		G += reward
		state = nextState

	returnSum = returnSum + G

	#Print every 10000 epiosed the average return
	if (episodeNum % 10000 == 0):
		print "Episode Num: ", episodeNum, "Average Return: ", returnSum/numEpisodes
print(blackjack.printPolicy(myGreedyPolicy))


#Reinitialize values
episodeNum = 0
returnSum = 0.00
testnumber = 1000000

#Now we run the deterministic policy 
for episodeNum in range(testnumber):
	#Being blackjack at start state
	state = blackjack.init()
	G = 0

	while state != -1:
		#Chooses the actions with the greatest value 
		action = myGreedyPolicy(state)

		#Samples a hand
		reward,nextState = blackjack.sample(state,action)

		G += reward
		state = nextState

	returnSum = returnSum + G

print(returnSum/testnumber)
	


		