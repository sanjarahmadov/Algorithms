import random
def generateRow(filename, n):
	res = []
	for i in range(n):
		res.append(str(random.randint(0,1)))
		res.append(",")
	res.pop()
	with open(filename, 'w') as f:
		print("".join(res), file = f)

def Main():
	generateRow("first_row.csv", 200)

if __name__ == "__main__":
	Main()
