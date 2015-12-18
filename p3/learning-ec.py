import mountaincar
import numpy
from Tilecoder import numTilings, tilecode, numTiles
from Tilecoder import numTiles as n
from pylab import *  #includes numpy

numRuns = 20
numEpisodes = 200
alpha = 0.5/numTilings
gamma = 1
lmbda = 0.9
Epi = Emu = epsilon = 0
n = numTiles * 3 # (4*(9*9)*3)
F = [-1]*numTilings

stepsPerEpisode = numpy.zeros(numEpisodes)
avgOfReturn = numpy.zeros(numEpisodes)
avgOfAllReturnDefault = numpy.zeros(numRuns/2)
avgOfAllReturnNonDefault = numpy.zeros(numRuns/2)
#avgOfAllReturnNonDefault = numpy.zeros(numRuns)

# Picks an action (First equation from specification)
def pickAction(theta,Q,Emu):
	actionOld = np.random.randint(3)
	action = np.random.choice([actionOld, numpy.argmax(Q)], p=[(epsilon), (1-epsilon)])
	return action

def Qs(F):
	Q = numpy.zeros(3)
	for a in range(0,3):
		for i in F:
			Q[a] = Q[a] + theta[i+a*323] # 323 is max (4*9*9-1), size(theta) = 972 = ((4*9*9) * 3 states)
	return Q

def writeF():
	fout = open('value', 'w')
	F = [0]*numTilings
	steps = 50
	for i in range(steps):
		for j in range(steps):
			tilecode(-1.2+i*1.7/steps, -0.07+j*0.14/steps, F)
			height = -max(Qs(F))
			fout.write(repr(height) + ' ')
		fout.write('\n')
	fout.close()

# Outputs into a file 'learningCurve' the "EPISODE NUMBER" "AVERAGE RETURN" "AVERAGE STEPS" for every episode
def write50Run():
	fout = open('learningCurve', 'w')
	for j in range(0,numEpisodes):
		fout.write(repr(j) + ' ' + repr(int(avgOfReturn[j]/numRuns)) + ' ' + repr(int(stepsPerEpisode[j]/numRuns)) + '\n')
	fout.close()


def avgStdDevCalc():
	stdErrDefault = numpy.std(avgOfAllReturnDefault, axis = 0)/numpy.sqrt(numRuns/2)
	stdErrNonDefault = numpy.std(avgOfAllReturnNonDefault, axis = 0)/numpy.sqrt(numRuns/2)
	#stdErrNonDefault = numpy.std(avgOfAllReturnNonDefault, axis = 0)/numpy.sqrt(numRuns)	
	meanDefault = numpy.mean(avgOfAllReturnDefault, axis = 0)
	meanNonDefault = numpy.mean(avgOfAllReturnNonDefault, axis = 0)
	print("Mean Default: ", meanDefault, "    Mean Non-Default: ", meanNonDefault, "\n")
	#print("Mean Non-Default: ", meanNonDefault, "\n")
	print("Std Err Default: ", stdErrDefault, "    Std Err Non-Default: ", stdErrNonDefault, "\n")
	#print("Std Err Non-Default: ", stdErrNonDefault, "\n")
	meanDiff = numpy.fabs(meanDefault - meanNonDefault)
	print("Mean Difference : ", meanDiff, "\n")
	maxDev = max(stdErrDefault, stdErrNonDefault)
	if (meanDiff > 2.5*maxDev):
		print("Mean difference GREATER than 2.5 times std Err: ", meanDiff, " " , 2.5*maxDev)
	else:
		print("Mean difference LESS than 2.5 times std Err: ", meanDiff, " " , 2.5*maxDev)


runSum = 0.0
for run in xrange(numRuns):
	theta = -0.01*rand(n)
	returnSum = 0.0
	for episodeNum in xrange(numEpisodes):
		G = 0
		state = mountaincar.init() # Initialize mountaincar
		 # Gets the initial position and velocity
		E = numpy.zeros(n)
		step = 0
		while state != None:
			position, velocity = state
			# Initialize F vector with position and velocity
			tilecode(position, velocity, F) 

			# Creates the Q vector using theta vector and F features
			Q = numpy.zeros(3)
			for a in range(0,3):
				for i in F:
					Q[a] = Q[a] + theta[i+a*323]

			# Picks an action, either argmax or random
			action = pickAction(theta,Q,epsilon) 
			
			# Samples to get reward and nextState
			reward, nextState = mountaincar.sample(state,action) 

			# Creates the delta variable and updates/creates the E vector
			delta = reward - Q[action]

			#Updates the eligibitly trace for that each indice returned by the tilecoder
			for i in F:
				E[i+action*323] = 1
			
			# if nextState is terminal...
			if nextState == None:
				theta = theta + alpha*delta*E
				state = nextState

			else:	

				# Gets new position and velocity from the new state
				position1, velocity1 = nextState 
	
				# Re-initialize F vector with new position and velocity
				tilecode(position1, velocity1, F) 

				#Create 
				Q1 = numpy.zeros(3)
				for a in range(0,3):
					for i in F:
						Q1[a] = Q1[a] + theta[i+a*323] # Re-creates the Q vector using theta vector and F features

				#Used for Q learning
				delta = delta + gamma*numpy.max(Q1)

				theta = theta + alpha*delta*E

				E = gamma*lmbda*E

				G += reward
				state = nextState
				step = step + 1
			
		#print "Episode: ", episodeNum, "Steps:", step, "Return: ", G
		returnSum = returnSum + G
		stepsPerEpisode[episodeNum] = stepsPerEpisode[episodeNum] + step
		avgOfReturn[episodeNum] = avgOfReturn[episodeNum] + G
	
	print "Average return:", returnSum/numEpisodes
	runSum += returnSum
	# Half the runs for the old epsilon and half for the new epsilon. CHANGE EPSILON HERE!
	if (run == numRuns/2):
		Epi = Emu = epsilon = 0.0 # Worked
		numTiles = 8
		n = numTiles * 3
		runSum = 0
	# Default Epsilon
	if (epsilon == 0):
		avgOfAllReturnDefault[run] = avgOfAllReturnDefault[run] + ((-1)*runSum/(numRuns/2))
	# Changed Epsilon
	if (epsilon != 0):
		avgOfAllReturnNonDefault[run-(numRuns/2)] = avgOfAllReturnNonDefault[run-(numRuns/2)] + ((-1)*runSum/(numRuns/2))
	#avgOfAllReturnNonDefault[run] = avgOfAllReturnNonDefault[run] + (runSum/(numRuns))
	
print "Overall performance: Average sum of return per run:", runSum/numRuns

# Generates file to run plot.py on for 3D plot
writeF()

# Generates learning curve data to run in Excel
write50Run()

# Extra Credit / Extra Extra Credit
avgStdDevCalc()
