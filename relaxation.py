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

M=comm.bcast(M,root=0)
comm.barrier()
#for elem in M: 
#	print elem

#if rank ==0:
#	for elem in M[0:4,:]: # rank 0
#		print "-",elem
#	for elem in M[2:6,:]: # rank 1 
#		print "*",elem
#	for elem in M[4:8,:]: # rank 2
#		print "%",elem
#        for elem in M[6:10,:]: # rank 3
#                print "+",elem

	# M[2*rank:2*rank+subROWS]

#distribute initial grid
subM = None
#if rank == 0:
#	for destination in xrange(size):
#		subM = M[2*destination:2*destination+subROWS,:]
#		comm.send(subM,dest=destination)

#subM = comm.recv(source=0,status = stat)
#sender = stat.Get_source()
#for elem in subM:
#print "Rank: %d\tSender: %d\tMessage:\n %s" % (rank,sender,subM)


sender = -5
subM = M[2*rank:2*rank+subROWS,:]
for elem in xrange(1,COLS-1):
	subM[1,elem] = (subM[1,elem-1]+subM[1,elem+1]+subM[0,elem]+subM[2,elem])/4.
	subM[2,elem] = (subM[2,elem-1]+subM[2,elem+1]+subM[1,elem]+subM[3,elem])/4.
#	print "Rank %d \t subM[1,%d]=%f,subM[2,%d]=%f" % (rank,elem,subM[1,elem],elem,subM[2,elem])
#print "New Rank: %d\tSender: %d\tMessage:\n %s" % (rank,sender,subM)
M[2*rank:2*rank+subROWS,:]=subM 

if rank == 0:
	print "Rank 0"
	for elem in M:
		print elem	
elif rank == size-1:
	print "Rank size-1"
else: 
	print "Else"


#for elem in xrange(1,size-1):
#	print elem
