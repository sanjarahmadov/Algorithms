class Rule30Class(object):
	"""
	Applies Rule 30 Cellular automation
	"""
	def __init__(self, r = 0):
		# We track the row index per instance in order to know the exact coordinates of matching six value pattern
		self._rowIndex = r

	def generateNextNode(self, a, b, c):
		"""
		Rule 30 logic is applied here
		
		:type a, b, c: Char
		:param a, b, c: First, second and third nodes respectively
	
		:type return: Char
		"""

		if ((a == '1' and b == '1' and c == '1')
		or  (a == '1' and b == '1' and c == '0')
		or  (a == '1' and b == '0' and c == '1')
		or  (a == '0' and b == '0' and c == '0')):
			return '0'
		else:
			return '1'
	
	def generateNextRow(self, row):
		"""
		Iterate over new row from second to last - 1 th element, and generate next node accoding to Rule 30
		
		:type row: List[Char]
		:param row: List of nodes

		:type return: List[Char]
		"""

		new_row = [None]*len(row)
		for i in range(1, len(row) - 1):
			new_row[i] = self.generateNextNode(row[i-1], row[i], row[i+1])
		new_row[0] = new_row[-2]
		new_row[-1] = new_row[1]
		
		self._rowIndex += 1
		return new_row
	
	def getCurrRow(self):
		return self._rowIndex

class SixValuePattern(object):
	"""
	Object representing 6 value pattern
	"""
	def __init__(self, pattern):
		simplePattern = "".join("".join(pattern.split("/")).split("-"))
		
		# Allows only 6 valued patterns for this problem
		assert (len(simplePattern) == 6), "Not a 6 value pattern"

		self._pattern = simplePattern

	def __str__(self):
		return self._pattern
	
	def pprint(self):
		"""
		Pretty Print for a six value pattern
		
		:type return: String
		"""
		res = []
		for i in range(len(self._pattern)):
			res.append(self._pattern[i])
			if i == len(self._pattern)//2 - 1:
				res.append("/")
			else:
				res.append("-")
		res.pop()
		return "".join(res)
	
	# We override operators so that we can use six valued patterns as dictionary keys
	def __hash__(self):
		return hash(self._pattern)
	
	def __eq__(self, other):
		return self._pattern == other._pattern

	def __ne__(self, other):
		return not self.__eq__(other)

def readCsv(filename):
	"""
	Read .csv file and make sure that it only contains one row

	:type filename: String
	:param filename: Name of a file from which we will read the first row in current directory
	
	:type return: List[Char]
	"""
	res = []
	with open(filename) as f:
		for line in f:
			line = line.strip("\n").split(",")
			res.append(line)
	assert(len(res) == 1), "Only first row should be present in csv file"
	return res

def newRow(ruleGenerator, row, pattern_map):
	"""
	Generate next row and update the pattern_map with occuring patterns

	:type ruleGenerator: Rule30Class
	:param ruleGenerator: Instance of a Rule30Class to generate nex row"

	:type row: List[char]
	:param row: List of nodes

	:type pattern_map: Dict
	:param pattern_map: Maps patterns to list of coordinates of the middle elements of second row in two row (six value) pattern

	:type return: (List[Char], Dict)
	"""
	new_row = ruleGenerator.generateNextRow(row)
	row_index = ruleGenerator.getCurrRow()
	start = 0
	for i in range(1, len(row) - 1):
		currPattern = "".join(row[start : i + 2] + new_row[start : i + 2])
		currSixValuePattern = SixValuePattern(currPattern)
		if currSixValuePattern not in pattern_map:
			pattern_map[currSixValuePattern] = []
		pattern_map[currSixValuePattern].append((i, row_index))
		start += 1

	return new_row, pattern_map

def get_pattern_occurrences(pattern_k, pattern_map):
	"""
	Returns list of coordinates for the pattern if it had occured in our result

	:type pattern_k: SixValuePattern
	:param pattern_k: Two row, six value pattern

	:type pattern_map: Dict
	:param pattern_map: Maps patterns to list of coordinates of the middle elements of second row in two row (six value) pattern

	:type return: List[Tuple[Int]]
	"""
	if pattern_k in pattern_map:
		return pattern_map[pattern_k]
	else:
		return "Such pattern does not exist"

def Main():
	A = readCsv("first_row.csv")
	if len(A[0]) < 3:
		print("At least three elements has to be in first row")
		return

	instance_of_rule30 = Rule30Class()
	pattern_map = dict()
	
	prev_row = A[0]
	print("".join(prev_row))
	for i in range(99):
		next_row, pattern_map = newRow(instance_of_rule30, prev_row, pattern_map)
		print("".join(next_row))
		prev_row = next_row

	patterns = [SixValuePattern("1-1-0/1-0-0"), SixValuePattern("1-1-0/1-0-1"), SixValuePattern("1-1-0/1-1-0")]
	for pattern_k in patterns:
		print(pattern_k.pprint())
		print(get_pattern_occurrences(pattern_k, pattern_map))

if __name__ == "__main__":
	Main()
