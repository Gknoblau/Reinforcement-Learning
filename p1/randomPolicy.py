#CMPUT 366 P1 Q1
#Greg Knoblauch
#Bryce Cartman

import blackjack
from pylab import *

numEpisodes = 1000000
returnSum = 0.0

for episodeNum in range(numEpisodes):
	state = blackjack.init()
	G = 0
	while state != -1:
		action = np.random.choice([0,1]) # Randomly chooses 1 or 0 action	
		reward,nextState = blackjack.sample(state,action)
		G += reward
		state = nextState

	returnSum = returnSum + G
	print "Episode: ", episodeNum, "Return: ", G
print "Average return: ", returnSum/numEpisodes
