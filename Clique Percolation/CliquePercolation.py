"""
Sanjar Ahmadov
Clique Percolation algorithm to find communities in a graph

Algorithm Structure
1. First we find k cliques in a graph, G, using Bron-Kerbosh Algorithm with pivoting and degeneracy ordering.
2. We create new graph, G*, where each clique is a node, and if any two cliques have more than k-1 common vertices, then there is an edge between these two clique nodes.
3. Connected cliques form a community. We check connectivity using BFS and see how many cliques are forming communities
4. We map from clique nodes, in G*, to intial verices, in G, and output which vertices are in which community

|V| - number of vertices
|E| - number of edges
"""

# Graph = Nodes: Neighbors
G = {	1: [2, 3, 4],
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

# Getting degeneracy order of graph G - Running Time O(|V|)
def degeneracy_ordering(G):
	deg_G = {}
	degenerate_order = []
	for key, value in G.items():
		deg_G[key] = len(value)
	
	# Ordering where vertice with lowest degree comes first
	while len(deg_G) > 0:
		v = min(deg_G.items(), key = lambda x: x[1])[0]
		degenerate_order.append(v)
		del deg_G[v]
		for i in G[v]:
			if i in deg_G:
				deg_G[i] -= 1
	return degenerate_order		

# Finding pivot u which has higest degree - Running Time O(|V|)
def pivot(G, S):
	max_v = 0
	max_n = 0
	for i in S:
		curr_n = len(G[i])
		if curr_n > max_n:
			max_n = curr_n
			max_v = i	
	return max_v

# Finding k-cliques using Bron-Kerbosh Algorithm - Running Time O(d*|V|*3^(d/3)) where d is sparseness measure
def k_clique(G, k, R, P, X, cliques, outermost):
	if len(P | X) == 0:
		if len(R) >= k:
			cliques.append(R[:])
		return None

	# Implementing 3rd version of the algorithm where in outermost level recursive call should be passed in degenerate order of graph
	if outermost is True:
		ordering = degeneracy_ordering(G)

	# In not outermost level we use pivoting vertice u having higest degree to reduce number of recursive calls
	else:
		u = pivot(G, P | X)
		ordering = list(P - set(G[u]))
	
	for v in ordering:
		N_v = set(G[v])
		k_clique(G, k, R + [v], P & N_v, X & N_v, cliques, False)
		P.remove(v)
		X.add(v)

	return cliques

# Use BFS to find communities in graph G - Running Time O(|E*|)
def find_communities(G):
	# Nodes will only hold unvisited vertices
	nodes = set(G.keys())
	
	# s is our queue
	s = []
	s.append(nodes.pop())

	# communities will hold all communities, while temp will hold one community at a time
	communities = []
	temp = []
	while len(s) > 0:
		curr = s.pop(0)
		# If currently visited node is unvisited list then remove it from the list
		if curr in nodes:
			nodes.remove(curr)

		temp.append(curr)
		for i in G[curr]:
			if i in nodes:
				s.append(i)

		# If no more node in queue check if there is any other node not connected to current community. If so, we are done with current community and we can move on to next one
		if len(s) == 0 and len(nodes) > 0:
			s.append(nodes.pop())
			communities.append(temp)
			temp = []

	# Last community currently in temp should be added to all communities list
	if len(temp) > 0:
		communities.append(temp)

	return communities

# Creating new graph from cliques were each clique is a node and connected to other clique if they share more than k-1 vertices - Running Time O(|V*|**2)
def cliques2graph(cliques, k):
	C_G = dict()
	for i in range(len(cliques)):
		curr = set(cliques[i])
		if i+1 not in C_G:
			C_G[i+1] = []
		for j in range(i+1, len(cliques)):
			if len((curr & set(cliques[j]))) >= k-1:
				C_G[i+1].append(j+1)

				if j+1 in C_G:
					C_G[j+1].append(i+1)
				else:
					C_G[j+1] = [i+1]	
	return C_G

# Main function which finds communities - Running Time O(d|V|3^d/3)
def clique_percolation(G, k):
	# Get cliqeus having more than k vertices
	R = []
	P = set(G.keys())
	X = set()
	cliques = k_clique(G, k, R, P, X, [], True)
	
	# When there is no cliques there is no community
	if not len(cliques) > 0:
		return -1

	# Create new graph, G*,  where each clique is a node and connected to other nodes if they share more than k-1 vertices
	C_G = cliques2graph(cliques, k)				

	# Find communities in a new graph G* using BFS
	communities = find_communities(C_G)
	
	# Map from G* to G to get individual vertices in each community
	communities_detailed = dict()
	for i in range(len(communities)):
		temp = set()
		curr_list = communities[i]
		for j in curr_list:
			temp = temp | set(cliques[j-1])
		communities_detailed[i+1] = temp
	
	return communities_detailed

# Graph G and k are given by user
print(clique_percolation(G, 4))
