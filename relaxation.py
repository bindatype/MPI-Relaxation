from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

COLS = 100
ROWS = 8192 
if size > ROWS:
        print("Not enough ROWS")
        exit()
subROWS=ROWS//size+2

def msgUp(subGrid):
        comm.send(subGrid[subROWS-2,:],dest=rank+1)
        subGrid[subROWS-1,:]=comm.recv(source=rank+1)
        return 0

def msgDn(subGrid):
        comm.send(subGrid[1,:],dest=rank-1)
        subGrid[0,:] = comm.recv(source=rank-1)
        return 0

def computeGridPoints(subGrid):
	for subROW in xrange(1,subROWS-1):
		for elem in xrange(1,COLS-1):
			subGrid[subROW,elem] = (subGrid[subROW,elem-1]
			+subGrid[subROW,elem+1]
			+subGrid[subROW-1,elem]
			+subGrid[subROW+1,elem])/4.
	return 0


# Set up initial grid on rank 0
Grid=None
if rank == 0:
#	M=numpy.array(range(COLS*(ROWS+2))).reshape((ROWS+2, COLS)).astype('float')
#	M=numpy.empty((ROWS+2, COLS)).astype('float')
	Grid=numpy.zeros((ROWS+2, COLS))
	Grid[0,:] = 1.
	Grid[:,0] = 1.
	initGrid = Grid

#distribute initial grid to other ranks
Grid=comm.bcast(Grid,root=0)

#parse out subgrids for each rank and delete Grid
subGrid = numpy.copy(Grid[(ROWS/size)*rank:(ROWS/size)*rank+subROWS,:])
del Grid

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
	print result[0]

