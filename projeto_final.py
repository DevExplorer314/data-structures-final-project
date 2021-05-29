# ISCTE-IUL
# 1º ano - Licenciatura em Ciência de Dados
# Projeto Final - U.C Estruturas de Dados e Algoritmos
# Grupo: João Portásio nº 94754 | Sandra Silva nº 98372 | Tiago Madeira nº 95088
#
# -------------------------------------------------- #

"""Modules"""
import csv
import networkx as nx

from Grupo_A2_heap_queue import AdaptableHeapPriorityQueue

"""
Implementação do TAD Grafo numa classe em Python, de acordo com a implementação prática nos exercícios do módulo 7
3.a) (usando dicionários de vértices e de adjacências) ou 
3.b) (um dicionário de vértices e uma estrutura de lista ligada para as adjacências implementada pelo grupo). 
Devem usar a interface e as classes Vertex e Edge, como indicado na aula.
"""


class Graph:
    '''
    Representation of a simple graph using an adjacency map.
    There exist nested Classes for Vertex and Edge objects and
    useful methods for vertex and edge, edge incidence and
    vertex degree retrieval plus edge and vertex insertion
    '''

    # == Class Vertex == #
    class Vertex:
        '''
        Class for representing vertex structure for a graph.
        '''
        __slots__ = '_element'

        def __init__(self, x):
            '''
            Do not call constructor directly. Use Graph's insert_vertex(x).
            '''
            self._element = x

        def element(self):
            '''
            Return element associated with this vertex.
            '''
            return self._element

        def __hash__(self):
            '''
            will allow vertex to be a map/set key
            '''
            return hash(self._element)

        def __repr__(self):
            return '{0}'.format(self._element)

        def __eq__(self, other):
            if isinstance(other, Graph.Vertex):
                return self._element == other._element
            return False

    # == Class Edge == #
    class Edge:
        '''
        Class for representing edge structure for a graph.
        '''
        __slots__ = '_origin', '_destination', '_weight'

        def __init__(self, u, v, x):
            '''
            Do not call constructor directly. Use Graph's insert_edge(x).
            '''
            self._origin = u
            self._destination = v
            self._weight = x

        def endpoints(self):
            '''
            Return (u,v) tuple for vertices u and v.
            '''
            return (self._origin, self._destination)

        def opposite(self, v):
            '''
            Return the vertex that is opposite v on this edge.
            '''
            return self._destination if self._origin == v else self._origin

        def element(self):
            '''
            Return element associated with this edge.
            '''
            return self._weight

        def __hash__(self):
            '''
            will allow edge to be a map/set key
            '''
            return hash((self._origin, self._destination))

        def __repr__(self):
            if self._weight is None:
                return '({0}, {1})'.format(self._origin, self._destination)
            return '({0}, {1}, {2})'.format(self._origin, self._destination, self._weight)

    # == Class Graph == #
    def __init__(self, directed=False):
        '''
        Create an empty graph (undirected, by default).
        Graph is directed if optional parameter is set to True.
        '''
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def __getitem__(self, arg):
        return self._incoming[arg]

    def is_directed(self):
        '''
        Return True if graph is directed
        '''

        return self._outgoing is not self._incoming

    def vertex_count(self):
        '''
        Return the vertices count
        '''
        return len(self._outgoing)

    def vertices(self):
        '''
        Return an iterator over the graph's vertices
        '''

        return self._outgoing.keys()

    def get_vertex(self, x):
        '''
        Return the graph's vertex with corresponding element
        equal to el. Return None on failure
        '''
        for vertex in self.vertices():
            if vertex.element() == x:
                return vertex

        return None

    def edges_count(self):
        '''
        Return the edges count
        '''

        edges = set()
        for secondary_map in self._outgoing.values():
            edges.update(secondary_map.values())
        return len(edges)

    def edges(self):
        '''
        Return a set of graph's edges
        '''
        edges = set()
        for secondary_map in self._outgoing.values():
            edges.update(secondary_map.values())
        return edges

    def get_edge(self, u, v):
        '''
        Return the edge from u to v
        '''
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        '''
        Return the number of incident vertices to v
        If graph is directed then handle the case of indegree
        '''

        inc = self._outgoing if outgoing else self._incoming
        return len(inc[v])

    def incident_edges(self, v, outgoing=True):
        '''
        Return all incident edges to node v.
        If graph is directed, handle the case of incoming edges
        '''
        inc = self._outgoing if outgoing else self._incoming
        if v not in inc:
            return None
        for edge in inc[v].values():
            yield edge

    def adjacent_vertices(self, v, outgoing=True):
        '''
        Return adjacent vertices to a given vertex
        '''
        if outgoing:
            if v in self._outgoing:
                return self._outgoing[v].keys()
            else:
                return None
        else:
            if v in self._incoming:
                return self._incoming[v].keys()
            else:
                return None

    def insert_vertex(self, x=None):
        '''
        Insert and return a new Vertex with element x
        '''
        for vertex in self.vertices():
            if vertex.element() == x:
                # raise exception if vertice exists in graph
                # exception can be handled from the class user
                return vertex

        v = self.Vertex(x)  # cria um objeto do tipo Vertex

        self._outgoing[v] = {}
        if self.is_directed:
            self._incoming[v] = {}

        return v

    def insert_edge(self, u, v, x=None):
        '''
        Insert and return a new Edge from u to v with auxiliary element x.
        '''
        if (v not in self._outgoing) or (v not in self._outgoing):
            # raise exception if one of vertices does not exist
            # exception can be handled from the class user
            raise Exception('One of the vertices does not exist')

        if self.get_edge(u, v):
            # no multiple edges
            # exception can be handled from the class user
            e = self.Edge(u, v, x)
            return e

        e = self.Edge(u, v, x)      # cria um objeto do tipo Edge

        self._outgoing[u][v] = e
        self._incoming[v][u] = e

        return e

    def remove_edge(self, u, v):
        if not self.get_edge(u, v):
            # exception for trying to delete non-existent edge
            # can be handled from class user
            raise Exception('Edge is already non-existent.')

        u_neighbours = self._outgoing[u]
        del u_neighbours[v]
        v_neighbours = self._incoming[v]
        del v_neighbours[u]

    def remove_vertex(self, x):
        '''
        Delete vertex and all its adjacent edges from graph
        '''

        if (x not in self._outgoing) and (x not in self._incoming):
            raise Exception('Vertex already non-existent')

        secondary_map = self._outgoing[x]
        for vertex in secondary_map:
            # delete reference to incident edges
            if self.is_directed():
                del self._incoming[vertex][x]
            else:
                del self._outgoing[vertex][x]
        # delete reference to the vertex itself
        del self._outgoing[x]

    def get_weight(self, v, outgoing=True):
        '''
        Return all incident edges to node v.
        If graph is directed, handle the case of incoming edges
        '''
        weights = {}
        queue = AdaptableHeapPriorityQueue()
        inc = self._outgoing if outgoing else self._incoming
        if v not in inc:
            return None
        for edge in inc[v].values():
            weights[v] = v
            weights[v] = queue.add(weights[v], edge.element())
            #weights.append(edge.element())
        print(weights)

    def printG(self):
        '''Mostra o grafo por linhas'''
        print('Grafo Orientado:', self.is_directed())

        '''Mostra o número de vertices'''
        print("Número de Vertices: {}".format(G.vertex_count()))

        '''Mostra o número de arestas'''
        print("Número de Arestas: {}".format(G.edges_count()))

        for v in self.vertices():
            print('\nUser: ', v, ' grau_in: ', self.degree(v, False), end=' ')
            if self.is_directed():
                print('grau_out: ', self.degree(v, False))
            for i in self.incident_edges(v):
                print(' ', i, end=' ')
            if self.is_directed():
                for i in self.incident_edges(v, False):
                    print(' ', i, end=' ')


"""2. Método de carregamento de dados de um ficheiro csv que obedeça ao seguinte formato:
    i) por linha existem 3 valores de dados - o 1.º e o 2.º indicam nomes de vértices e o 3.º um peso. 
    ii) A 1.ª linha do ficheiro indica o nome das colunas.
    Nota importante: caso não exista 3ª coluna, devem assumir que o grafo não é pesado e lidar com essa situação sem erro
"""

""" 3. Proceda ao Carregamento de dados do ficheiro Github.csv (no e-Learning) """
def read_csv(filename):
    G = Graph()  # cria um objeto do tipo Graph

    with open(filename, 'r') as csv_file:  # abre o ficheiro csv
        data = csv.reader(csv_file)
        next(data)  # ignora a primeira linha do ficheiro

        for linha in data:  # por cada linha no ficheiro
            id_origem = linha[0]  # a origem é a primeira coluna do ficheiro
            id_destino = linha[1]  # o destino é a segunda coluna do ficheiro
            peso = linha[2] if len(linha) > 2 else 1       # se não existir uma terceira coluna do ficheiro
                                                           # assume-se que o peso das arestas é 1

            v_origem = G.insert_vertex(id_origem)  # insere o vertex no grafo
            v_destino = G.insert_vertex(id_destino)  # insere o vertex no grafo

            G.insert_edge(v_origem, v_destino, int(peso))  # insere a aresta no grafo

    return G

""" 5. Implementação de métodos para determinar caminhos mais curtos num grafo """

""" (b) usando os pesos nas arestas"""
def shortest_path_lengths(G, src):
    '''Aplicação do algoritmo de Dijkstra'''
    d = {}
    cloud = {}
    pq = AdaptableHeapPriorityQueue()
    pqlocator = {}
    source = Graph.Vertex(src)
    for v in G.vertices():
        if v == source:
            d[v] = 0
        else:
            d[v] = float('inf')
        pqlocator[v] = pq.add(d[v], v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key
        del pqlocator[u]
        for e in G.incident_edges(u):
            v = e.opposite(u)
            if v not in cloud:
                wgt = e.element()
                if d[u] + wgt < d[v]:
                   d[v] = d[u] + wgt
                   pq.update(pqlocator[v], d[v], v)

    return cloud


""" 6. Implementação, pelo menos, das medidas de centralidade: centralidade de grau (degree centrality) e centralidade de proximidade
(closeness). """

def degree_centrality(G):
    '''Centralidade de grau'''
    degrees = {}
    vertex_count = G.vertex_count()     # número de vertices do grafo

    for v in G.vertices():      # Percorre os vertices no grafo
        vertex_degree = G.degree(G.get_vertex(str(v)))     # Calcula o grau de cada vertice
        formula = vertex_degree / (vertex_count - 1)       # Formula para calcular o grau de centralidade
        degrees[v] = round(formula, 2)      # Adiciona ao dicionário um par de {key: value}, onde a key é o vertice e o value é o grau de centralidade desse vertice
    return degrees


def closeness_centrality(G, src):
    '''Centralidade de proximidade'''
    distances = []
    short = shortest_path_lengths(G, src)
    vertex_number = G.vertex_count()
    for value in short.values():
        if value != float('inf'):
            distances.append(value)
    soma = sum(distances)
    if soma != 0:
        formula = (vertex_number - 1) / soma
        return formula
    else:
        raise Exception("Erro!")

def sort_tuple(tup):
    '''Função para ordenar a lista de tuplos pelo seu segundo item'''
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if tup[j][1] < tup[j + 1][1]:
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

"""7. a) O Top 10 dos vértices mais interligados na sua rede."""
def top_degree_centrality(G):
    top = []
    degrees = degree_centrality(G)
    for key, value in degrees.items():
        top.append((str(key), value))
    return sort_tuple(top[:10])


"""7. b) O Top 10 dos vértices que apresentam maior proximidade aos restantes."""
def top_closeness(G):
    top = []
    for v in G.vertices():
        d = closeness_centrality(G, str(v))
        top.append((v, round(d, 2)))
    return sort_tuple(top[:10])


def DFS(graph, start, dest):
    stack = list()
    visited = list()
    s = Graph.Vertex(start)
    d = Graph.Vertex(dest)
    stack.append(s)
    visited.append(s)
    print('Visited', s)
    result = ["Not reachable", list()]
    while stack:
        node = stack.pop()
        if node == d:
            print('Destination node found', node)
            result[0] = 'Reachable'
            break
        print(node,'Is not a destination node')
        for child in graph[node]:
            if child not in visited:
                visited.append(child)
                stack.append(child)
    result[1] = visited
    return result

if __name__ == "__main__":

    # Ficheiro CSV
    filename = "Github1.csv"

    # Criação do objeto grafo
    G = read_csv(filename)



    #top_degree_centrality(G)

    #top_closeness(G)

    #shortestPathBFS(G, "Murphy", "Bradley")
    #shortestPathBFS(G, "Murphy", "Murphy")
    # centrality_degree(G, "Carlos")

    # Calcular o grau de centralidade de cada vértice
    # degree_centrality(G)

    #shortest_path_lengths(G, "Abraham")

    # Remove um Vertex
    # G.remove_vertex(G.get_vertex("Abraham"))

    # Remove um Edge
    #G.remove_edge("Abrams", "Pereira")

    # Shortest path
    # shortest_path_lengths(G, )

    # Print do grafo
    # G.printG()
