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

# Set up initial grid on rank 0
M=None
if rank == 0:
	M=numpy.array(range(COLS*(ROWS+2))).reshape((ROWS+2, COLS)).astype('float')
#	M=numpy.empty((ROWS+2, COLS)).astype('float')
#	M=numpy.zeros((ROWS+2, COLS))
	M[0,:] = 1.
	M[:,0] = 1.

#distribute initial grid to other ranks
M=comm.bcast(M,root=0)
comm.barrier()

for i in xrange(10):
	#parse out subgrids for each rank and sweep thru
	subM = M[(ROWS/size)*rank:(ROWS/size)*rank+subROWS,:]
	for subROW in xrange(1,subROWS-1):
		for elem in xrange(1,COLS-1):
			subM[subROW,elem] = (subM[subROW,elem-1]+subM[subROW,elem+1]+subM[subROW-1,elem]+subM[subROW+1,elem])/4.
	M[2*rank:2*rank+subROWS,:]=subM 
	#exhange edges for next interation
	if rank == 0:
		comm.send(M[ROWS*(rank+1)/size,:],dest=rank+1)
		M[ROWS*(rank+1)/size+1,:]=comm.recv(source=rank+1)
	elif rank == size-1:
		comm.send(M[ROWS*rank/size+1,:],dest=rank-1)
		M[ROWS*(rank)/size,:]=comm.recv(source=rank-1)
	else: 
		comm.send(M[ROWS*rank/size+1,:],dest=rank-1)
		comm.send(M[ROWS*(rank+1)/size,:],dest=rank+1)
		M[ROWS*(rank)/size,:]=comm.recv(source=rank-1)
		M[ROWS*(rank+1)/size+1,:]=comm.recv(source=rank+1)
	#print current status
#	print "Rank:0 %d\t M: %s " %(rank,M)



subM = M[(ROWS/size)*rank:(ROWS/size)*rank+subROWS,:]
newM=comm.gather(subM,root=0)
if rank == 0:
	print "Rank:0 %d\t M: %s " %(rank,newM)
