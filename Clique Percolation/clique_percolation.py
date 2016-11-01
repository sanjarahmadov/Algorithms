# Graph = Nodes: Neighbors
G = {	1: [5, 2],
	2: [5, 1],
	3: [2, 4],
	4: [5, 3, 6],
	5: [4, 2, 1],
	6: [4]
}

GG = {	1: [2, 3, 4],
	2: [1, 3, 4, 10, 9],
	3: [1, 2, 4, 5, 6],
	4: [1, 2, 3, 9, 8, 7, 6, 5],
	5: [3, 4, 9, 7, 6],
	6: [5, 3, 4, 9, 7],
	7: [6, 5, 4, 9, 8],
	8: [7, 4, 9],
	9: [2, 4, 5, 6, 7, 8, 10],
	10: [2, 9]
}

n = 0

def degeneracy_ordering(G):
	deg_G = {}
	degenerate_order = []

	for key, value in G.items():
		deg_G[key] = len(value)
	
	while len(deg_G) > 0:
		v = min(deg_G.items(), key = lambda x: x[1])[0]
		degenerate_order.append(v)
		del deg_G[v]
		
		for i in G[v]:
			if i in deg_G:
				deg_G[i] -= 1
	return degenerate_order		

def pivot(G, S):
	max_v = 0
	max_n = 0
	for i in S:
		curr_n = len(G[i])
		if curr_n > max_n:
			max_n = curr_n
			max_v = i	
	return max_v

def k_clique(G, k, R, P, X, cliques, outermost):
	global n
	n += 1
	print(n)
	if len(P | X) == 0:
		if len(R) >= k:
			cliques.append(R[:])
		return None
	

	if outermost is True:
		ordering = degeneracy_ordering(G)
	else:
		u = pivot(G, P | X)
		ordering = list(P - set(G[u]))
	
	for v in ordering:
		
		N_v = set(G[v])
		k_clique(G, k, R + [v], P & N_v, X & N_v, cliques, False)
		P.remove(v)
		X.add(v)

	return cliques


def clique_percolation(G, k):
	# Get cliqeus having more than k vertices
	R = []
	P = set(G.keys())
	X = set()

	cliques = k_clique(G, k, R, P, X, [], True)
	
	return cliques

print(clique_percolation(GG, 2))
