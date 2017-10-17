from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

COLS = 4
ROWS = 8


if size > ROWS:
	print("Not enough ROWS")
	exit()
if rank == 0:
	M=numpy.array(range(COLS*ROWS)).reshape((ROWS, COLS))
#	M=numpy.empty((ROWS+2, COLS))
	M[0,:] = 1
	M[:,0] = 1
	for i in M: 
   		print i

	# Init Grid

#if rank ==0:
#	for i in M[:,0]:
#		print i
