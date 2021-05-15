# ISCTE-IUL
# 1º ano - Licenciatura em Ciência de Dados
# Projeto Final - U.C Estruturas de Dados e Algoritmos
# Grupo: João Portásio nº 94754 | Sandra Silva nº 98372 | Tiago Madeira nº 95088
#
# -------------------------------------------------- #

"""Modules"""
import csv

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
            return hash(id(self))

        def __repr__(self):
            return '{0}'.format(self._element)

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

        def endPoints(self):
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
            return hash(id(self))

        def __repr__(self):
            if self._weight is None:
                return '({0}, {1})'.format(self._origin, self._destination)
            return '({0}, {1}, {2})'.format(self._origin, self._destination, self._weight)

    # == Class Graph == #
    def __init__(self, directed=False):
        '''
        Create an empty graph (undirected, by default).
        Graph is directed if optional paramter is set to True.
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

    def get_vertex(self, el):
        '''
        Return the graph's vertex with corresponding element
        equal to el. Return None on failure
        '''
        for vertex in self.vertices():
            if vertex.element() == el:
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
            if (vertex.element() == x):
                # raise exception if vertice exists in graph
                # exception can be handled from the class user
                raise Exception('Vertice already exists')

        v = self.Vertex(x)

        self._outgoing[v] = {}
        if self.is_directed:
            self._incoming[v] = {}

        return v

    def insert_edge(self, u, v, x=None):
        """TODO: Validar a questão dos duplicados"""
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
            raise Exception('Edge already exists.')

        e = self.Edge(u, v, x)

        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def delete_edge(self, u, v):
        if not self.get_edge(u, v):
            # exception for trying to delete non-existent edge
            # can be handled from class user
            raise Exception('Edge is already non-existent.')

        u_neighbours = self._outgoing[u]
        del u_neighbours[v]
        v_neighbours = self._incoming[v]
        del v_neighbours[u]

        return None

    def delete_vertex(self, x):
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
        return None

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

    G = Graph()

    with open(filename, 'r') as csv_file:
        data = csv.reader(csv_file)

        for linha in data:
            id_origem = linha[0]
            id_destino = linha[1]
            peso = linha[2] if len(linha) > 2 else 1 # None

            v_origem = G.insert_vertex(id_origem)
            v_destino = G.insert_vertex(id_destino)

            G.insert_edge(v_origem, v_destino, peso)

    return G

""" 5. Implementação de métodos para determinar caminhos mais curtos num grafo """

"""(a) sem usar os pesos nas arestas)"""

""" (b) usando os pesos nas arestas"""


def dijkstra_path(grafo, origem, fim):  # retorna a menor distancia de um No origem até um No destino e o caminho até ele

    controle = {}
    distanciaAtual = {}
    noAtual = {}
    naoVisitados = []
    atual = origem
    noAtual[atual] = 0

    for vertice in G.vertices():
        naoVisitados.append(vertice)  # inclui os vertices nos não visitados
        distanciaAtual[vertice] = float('inf')  # inicia os vertices como infinito

    distanciaAtual[atual] = [0, origem]

    naoVisitados.remove(atual)

    while naoVisitados:
        for vizinho, peso in grafo[atual].items():
            pesoCalc = peso + noAtual[atual]
            if distanciaAtual[vizinho] == float("inf") or distanciaAtual[vizinho][0] > pesoCalc:
                distanciaAtual[vizinho] = [pesoCalc, atual]
                controle[vizinho] = pesoCalc
                print(controle)

        if controle == {}: break
        minVizinho = min(controle.items(), key=lambda x: x[1])  # seleciona o menor vizinho
        atual = minVizinho[0]
        noAtual[atual] = minVizinho[1]
        naoVisitados.remove(atual)
        del controle[atual]

if __name__ == "__main__":

    # Ficheiro CSV
    filename = "Data_Facebook_TESTE.csv"

    # Criação do objeto grafo
    G = read_csv(filename)

    dijkstra_path(G, "Lynch", "Arnold")
    # Print do grafo
    #G.printG()
