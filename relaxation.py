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
#print subROWS

M=None
if rank == 0:
	M=numpy.array(range(COLS*(ROWS+2))).reshape((ROWS+2, COLS)).astype('float')
#	M=numpy.empty((ROWS+2, COLS)).astype('float')
#	M=numpy.zeros((ROWS+2, COLS))
	M[0,:] = 1.
	M[:,0] = 1.

#distribute initial grid
M=comm.bcast(M,root=0)
comm.barrier()

subM = None

sender = -5
subM = M[2*rank:2*rank+subROWS,:]
for elem in xrange(1,COLS-1):
	subM[1,elem] = (subM[1,elem-1]+subM[1,elem+1]+subM[0,elem]+subM[2,elem])/4.
	subM[2,elem] = (subM[2,elem-1]+subM[2,elem+1]+subM[1,elem]+subM[3,elem])/4.
#	print "Rank %d \t subM[1,%d]=%f,subM[2,%d]=%f" % (rank,elem,subM[1,elem],elem,subM[2,elem])
#print "New Rank: %d\tSender: %d\tMessage:\n %s" % (rank,sender,subM)
M[2*rank:2*rank+subROWS,:]=subM 


if rank == 0:
	comm.send(M[subROWS-2,:],dest=rank+1)
	M[subROWS-1,:]=comm.recv(source=rank+1)
elif rank == size-1:
	comm.send(M[2*rank+1,:],dest=rank-1)
	M[ROWS-subROWS,:]=comm.recv(source=rank-1)
else: 
	comm.send(M[rank*subROWS,:],dest=rank-1)
	comm.send(M[(rank+0)*subROWS,:],dest=rank+1)
	M[ROWS-subROWS,:]=comm.recv(source=rank-1)
	M[2*rank+subROWS-1,:]=comm.recv(source=rank+1)

print "Rank: %d\t M: %s " %(rank,M)

#for elem in xrange(1,size-1):
#	print elem
