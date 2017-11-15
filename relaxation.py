#from memory_profiler import profile
from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

# Set global variables
COLS = 100
ROWS = 8192 
if size > ROWS:
        print("Not enough ROWS")
        exit()
subROWS=ROWS//size+2

# Function definitions 
#@profile
def msgUp(subGrid):
	# Sends and Recvs rows with Rank+1
        comm.send(subGrid[subROWS-2,:],dest=rank+1)
        subGrid[subROWS-1,:]=comm.recv(source=rank+1)
        return 0

def msgDn(subGrid):
	# Sends and Recvs rows with Rank-1
        comm.send(subGrid[1,:],dest=rank-1)
        subGrid[0,:] = comm.recv(source=rank-1)
        return 0

def computeGridPoints(subGrid):
	for subROW in xrange(1,subROWS-1):
		for elem in xrange(1,COLS-1):
			subGrid[subROW,elem] = (
			subGrid[subROW,elem-1]
			+subGrid[subROW,elem+1]
			+subGrid[subROW-1,elem]
			+subGrid[subROW+1,elem])/4.
	return 0

# All workers initialize a zero-valued subgrid and 
# boundary conditions are assigned by rank as below. 
# This minimizes memory and communication compared to 
# bcast or scatter.
subGrid = numpy.zeros((subROWS, COLS))

# BC for all ranks.
subGrid[:,0] = 1.

# BC for rank 0.
if rank ==0:
	subGrid[0,:] = 1

# The main body of the algorithm
#compute new grid and pass rows to neighbors
for i in xrange(100):
	computeGridPoints(subGrid)
	#exhange edge rows for next interation	
	if rank == 0:
		msgUp(subGrid)
	elif rank == size-1:
		msgDn(subGrid)
	else:	
		msgUp(subGrid)
		msgDn(subGrid)		


newGrid=comm.gather(subGrid[1:subROWS-1,:],root=0)

if rank == 0:
	result= numpy.vstack(newGrid)
#	print numpy.vstack(initGrid)
	print result[-1]

