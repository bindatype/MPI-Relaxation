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
subROWS=ROWS//size+2
print subROWS

if rank == 0:
	M=numpy.array(range(COLS*(ROWS+2))).reshape((ROWS+2, COLS))
#	M=numpy.empty((ROWS+2, COLS))
	M[0,:] = 1
	M[:,0] = 1
	for elem in M: 
   		print elem

if rank ==0:
	for elem in M[0:4,:]: # rank 0
		print "-",elem
	for elem in M[2:6,:]: # rank 1 
		print "*",elem
	for elem in M[4:8,:]: # rank 2
		print "%",elem
        for elem in M[6:10,:]: # rank 3
                print "+",elem

	# M[2*rank:2*rank+subROWS]
