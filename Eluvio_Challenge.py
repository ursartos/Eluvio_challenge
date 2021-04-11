import sys

### complete graph to map every longest byte strand between all valid combinations of file pairs ###
# each vertex is a file in Graph with a name and array of bytes in the file
# each edge is a longest byte strand in Graph with the file vertices it compares, the length of the byte strand,
# offsets for both vertices it connects to, and the byte value of the strand for breaking ties
class Graph():
	def __init__(self, input_array, file_names):
		self.vertices = []
		for i in range(len(input_array)):
			self.vertices.append(Node(file_names[i], input_array[i]))

		self.edges = []
		for i in range(0,len(self.vertices)):
			for j in range(i+1, len(self.vertices)):
				self.edges.append(Edge(self.vertices[i],self.vertices[j]))

class Edge():
	def __init__(self, left, right):
		self.left = left
		self.right = right
		self.len = 0
		self.left_offset = 0
		self.right_offset = 0
		self.byte = 0

	def set_len(self, len):
		self.len = len

	def set_offsets(self, offset_left, offset_right):
		if (self.left_offset < offset_left):
			self.left_offset = offset_left
		if (self.right_offset < offset_right):
			self.right_offset = offset_right

	def set_byte(self, byte):
		self.byte = byte

class Node():
	def __init__(self, name, byte_array):
		self.name = name
		self.byte_array = byte_array

###  called by graph_pairs function with the byte_array for 2 different files and finds the max strand of bytes between them
# also returning offsets of the byte strand in both files, and the value of returned byte strand ###
# Dynamic programming running in O(ab) time where a = len(A) and b = len(B)
# DP table implemented as a dictionary to store only non-zero values and save memory on this larger 2^8 sized alphabet
# also, to reduce memory from  O(ab) to O(min(a,b)), DP dictionary is only ever holding the current and previous row of the table
def least_of_two(A, B):
	a,b = len(A), len(B)
	C = {}
	max_len = 0
	offset_A = 0
	offset_B = 0
	curr_max = []
	k = -1

	for i in range(a):
		k *= -1
		for j in range(b):
			if (A[i] == B[j]):
				if (i==0 or j == 0 or not -1*k*(j-1) in C):
					C[k*j] = 1
				else:
					C[k*j] = C[-1*k*(j-1)] + 1
				if (C[k*j] > max_len):
					max_len = C[k*j]
					curr_max = A[i - max_len + 1:i]
					offset_A = i - max_len + 1
					offset_B = j - max_len + 1
	max_byte = 0
	for i in range(len(curr_max),0):
		max_byte = max_byte or curr_max[i]
		max_byte = max_byte << 2

	return max_len, offset_A, offset_B, max_byte

###  called by main function with arguments sys.argv for file names and 2 dimensional input_array 
# containing the contents of each file separated by byte ###
# For number of files, n, least_of_two is run n(n-1)/2 times (number of edges in a complete graph) each run taking O(k^2) where k is
# the number of bytes in the largest file.
def graph_pairs(input_array, args):
	G = Graph(input_array, args)
	max_val = 0
	max_list = []
	for edge in G.edges:
		length, offset_left, offset_right, byte = least_of_two(edge.left.byte_array, edge.right.byte_array)
		edge.set_len(length)
		edge.set_offsets(offset_left, offset_right)
		edge.set_byte(byte)
		if (edge.len > max_val):
			max_val = edge.len
			max_list = [edge]
		elif (edge.len == max_val and edge.byte == max_list[0].byte):
			max_list.append(edge)
	return max_list

###  main function, called with argument sys.argv ###
# For number of bytes in the largest file, k, and number of files, n, main runs in O(n^2*k^2) time with O(nk) space complexity to hold input_array
def main(args):
	input_array = [0]*(len(args)-1)
	for i in range(1,len(args)):
		file = open("samples/" + str(args[i]), "rb")
		byte_str = file.read(1)
		byte_list = []
		while byte_str:
			byte_list.append(byte_str)
			byte_str = file.read(1)
		input_array[i-1] = byte_list
		file.close()

	max_list = graph_pairs(input_array, args[1:])
	print("length of the longest common strand of bytes in at least 2 files is " + str(max_list[0].len))
	print("The files names that contain this longest common strand along with the offsets in bytes for the strand in each are:")
	files = []
	for edge in max_list:
		left_node = (edge.left.name, edge.left_offset)
		if (left_node not in files):
			files.append(left_node)
			print(left_node)
		right_node = (edge.right.name, edge.right_offset)
		if (right_node not in files):
			files.append(right_node)
			print(right_node)

main(sys.argv)