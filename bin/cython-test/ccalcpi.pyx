
from cython.parallel import parallel, prange
cimport openmp
from libc.stdlib cimport malloc, free
import cython

def calcpi(int n):
	cdef double result = 0.0
	cdef int num_threads
	cdef int i, si
	#s = Decimal(1)
	#pi = Decimal(3)
	
	#n = 5000
	with nogil, parallel(num_threads=4):
		#for i in range(2, n * 2, 2):
		for i in prange(2, n * 2, 2):
			#pi = pi + s * ( Decimal(4) / (Decimal(i) * (Decimal(i) + Decimal(1)) * (Decimal(i) + Decimal(2)) ) )
			si = 1 if  ((i/2) % 2 == 1) else -1
			result += 4.0 * si  /  ( i * ( i + 1.0) * ( i + 2.0) )
			#print result
			#s = -1 * s
	return result + 3
