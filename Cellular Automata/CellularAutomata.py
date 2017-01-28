class Rule30Class(object):
	"""
	Applies Rule 30 Cellular automation
	"""
	def __init__(self, r = 0):
		self._rowIndex = r

	def generateNextNode(self, a, b, c):
		if ((a == '1' and b == '1' and c == '1')
		or  (a == '1' and b == '1' and c == '0')
		or  (a == '1' and b == '0' and c == '1')
		or  (a == '0' and b == '0' and c == '0')):
			return '0'
		else:
			return '1'
	
	def generateNextRow(self, row):
		
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
	def __init__(self, pattern):
		simplePattern = "".join("".join(pattern.split("/")).split("-"))
		assert (len(simplePattern) == 6), "Not a 6 value pattern"
		self._pattern = simplePattern

	def __str__(self):
		return self._pattern
	
	def pprint(self):
		res = []
		for i in range(len(self._pattern)):
			res.append(self._pattern[i])
			if i == len(self._pattern)//2 - 1:
				res.append("/")
			else:
				res.append("-")
		res.pop()
		return "".join(res)
	
	def __hash__(self):
		return hash(self._pattern)
	
	def __eq__(self, other):
		return self._pattern == other._pattern

	def __ne__(self, other):
		return not self.__eq__(other)

def readCsv(filename):
	res = []
	with open(filename) as f:
		for line in f:
			line = line.strip("\n").split(",")
			res.append(line)
	assert(len(res) == 1), "Only first row should be present in csv file"
	return res

def newRow(ruleGenerator, row, pattern_map):
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
	if pattern_k in pattern_map:
		return pattern_map[pattern_k]
	else:
		return "Such a pattern does not exist"

def Main():
	A = readCsv("first_row.csv")
	instance_of_rule30 = Rule30Class()
	pattern_map = dict()
	
	prev_row = A[0]
	print("".join(prev_row))
	for i in range(99):
		next_row, pattern_map = newRow(instance_of_rule30, prev_row, pattern_map)
		print("".join(next_row))
		prev_row = next_row
	print(len(pattern_map))	
	patterns = [SixValuePattern("1-1-0/1-0-0"), SixValuePattern("1-1-0/1-0-1"), SixValuePattern("1-1-0/1-1-0")]
	for pattern_k in patterns:
		print(pattern_k.pprint())
		print(get_pattern_occurrences(pattern_k, pattern_map))

if __name__ == "__main__":
	Main()
