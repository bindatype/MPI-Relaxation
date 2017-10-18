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

if rank == 0:
	M=numpy.array(range(COLS*(ROWS+2))).reshape((ROWS+2, COLS)).astype('float')
#	M=numpy.empty((ROWS+2, COLS)).astype('float')
#	M=numpy.zeros((ROWS+2, COLS))
	M[0,:] = 1.
	M[:,0] = 1.
#	M.astype('float')
	for elem in M: 
   		print elem
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
message = None
if rank == 0:
	for destination in xrange(size):
		message = M[2*destination:2*destination+subROWS,:]
		comm.send(message,dest=destination)

message = comm.recv(source=0,status = stat)
sender = stat.Get_source()

#for elem in message:
print "Rank: %d\tSender: %d\tMessage:\n %s" % (rank,sender,message)

for elem in xrange(1,COLS-1):
	message[1,elem] = (message[1,elem-1]+message[1,elem+1]+message[0,elem]+message[2,elem])/4.
	message[2,elem] = (message[2,elem-1]+message[2,elem+1]+message[1,elem]+message[3,elem])/4.
#	print "Rank %d \t message[1,%d]=%f,message[2,%d]=%f" % (rank,elem,message[1,elem],elem,message[2,elem])
print "New Rank: %d\tSender: %d\tMessage:\n %s" % (rank,sender,message)

#M = comm.gather(message, root=0)
#if rank == 0:
#        for elem in M:
#                print "+",elem
