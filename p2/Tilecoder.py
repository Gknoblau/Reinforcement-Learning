import math

numTilings = 8
    
def tilecode(x,y,tileIndices):
    # write your tilecoder here (5 lines or so)
	for n in range(0, numTilings):
		# 0.6 because 6/10 (ie: 6:10 ratio of small tiles), add x,y to determine new 
		# coordinates. 
		distX = x + n*(0.6/numTilings)
		distY = y + n*(0.6/numTilings)
		
		# Always assume 11x11 grid, however, if the newY/(6/10) is greater than 0.6,
		# ie: 0.625, it is OUTSIDE the 6x6 input space. If it is outside, we add a new
		# row of 11 tiles and the corresponding distX offset.
		tileIndices[n] = int(n*(11*11) + (11*math.floor(distY/0.6)) + math.floor(distX/0.6))
    
def printTileCoderIndices(x,y):
    tileIndices = [-1]*numTilings
    tilecode(x,y,tileIndices)
    print 'Tile indices for input (',x,',',y,') are : ', tileIndices

# Comment out for Part 2 of the assignment\

#printTileCoderIndices(0.1,0.1)
#printTileCoderIndices(4.0,2.0)
#printTileCoderIndices(5.99,5.99)
#printTileCoderIndices(4.0,2.1)
    
