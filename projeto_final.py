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

# == Class Vertex == #
class Vertex:
    """Estrutura de Nó para um grafo: um elemento que é o identificador deste nó"""

    __slots__ = "_element"

    def __init__(self, x):
        """O vértice será inserido no Grafo usando o método insert_vertex(x) que cria um Vertex"""
        self._element = x

    def vertice(self):
        """Devolve o nome deste vértice; esconde o verdadeiro identificador do atributo"""
        return self._element

    """Comparação de vértices"""

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self._element == other.vertice()
        return False

    def __str__(self):
        return '{0}'.format(self._element)

    def __hash__(self):
        """Referência de memória (usada por causa das keys dos dicionários)"""
        return hash(id(self))  # devolve um inteiro que identifica este vértice como uma chave num dicionário


# == Class Edge == #
class Edge:
    """Estrutura de Aresta para um Grafo: (origem, destino) e seu peso """

    def __init__(self, u, v, p=None):
        self._origin = u
        self._destination = v
        self._weight = p

    def __hash__(self):
        # para associar a aresta a uma chave para um dicionário
        return hash((self._origin, self._destination))

    def __repr__(self):
        return '({0},{1}, {2})'.format(self._origin, self._destination, self._weight)

    def endpoints(self):
        """Return (u,v) tuple for vertices u and v."""
        return self._origin, self._destination

    def opposite(self, v):
        """Return the vertex that is opposite v on this edge."""
        return self._origin if v is self._destination else self._origin

    def cost(self):
        """Return the value associated with this edge."""
        return self._weight

    def show_edge(self):
        print('(', self._origin, ', ', self._destination, ') com peso', self._weight)


# == Class Graph == #
class Graph:
    """Representação de um grafo usando mapeamentos de adjacências (associações) com dictionaries"""

    def __init__(self, directed=False):
        """Cria um grafo vazio (dicionário de _vertices); é orientado se o parâmetro directed tiver o valor True"""
        self._directed = directed
        self._number = 0  # quantidade de nós no Grafo
        self._vertices = {}  # dicionário com chave vértice e valor dicionário de adjacências

    def insert_vertex(self, x):
        """Insere e devolve um novo vértice com o elemento x"""
        v = Vertex(x)
        self._vertices[v] = {}  # inicializa o dicionário de adjacências a vazio
        return v

    def insert_edge(self, u, v, x):
        """Cria u e v e insere e devolve uma nova aresta entre u e v com peso x"""
        e = Edge(u, v, x)
        self._vertices[u][v] = e  # vai colocar nas adjacências de u
        self._vertices[v][u] = e  # e nas adjacências de v (para facilitar a procura de todos os arcos incidentes)

    def incident_edges(self, v, outgoing=True):
        """Gerador: indica todas as arestas (outgoing) incidentes em v
           Se for um grafo dirigido e outgoing for False, devolve as arestas em incoming
        """
        for edge in self._vertices[v].values():  # para todas as arestas relativas a v:
            if not self._directed:
                yield edge
            else:  # senão deve ir procurar em todas as arestas para saber quais entram ou saiem
                x, y = edge.endpoints()
                if (outgoing and x == v) or (not outgoing and y == v):
                    yield edge

    def is_directed(self):
        """com base na criação original da instância, devolve True se o Grafo é dirigido; False senão """
        return self._directed  # True se os dois contentores são distintos

    def vertex_count(self):
        """Devolve a quantidade de vértices no grafo"""
        return self._number

    def vertices(self):
        """Devolve um iterável sobre todos os vértices do Grafo"""
        return self._vertices.keys()

    def edge_count(self):
        """Devolve a quantidade de arestas do Grafo"""
        total = sum(len(self._vertices[v]) for v in self._vertices)
        # for undirected graphs, make sure not to double-count edges
        return total if self._directed else total // 2

    def edges(self):
        """Devolve o conjunto de todas as arestas do Grafo"""
        result = set()  # avoid double-reporting edges in undirected graph
        for secondary_map in self._vertices.values():
            result.update(secondary_map.values())  # add edges to resulting set
        return result

    def get_edge(self, u, v):
        """Devolve a aresta que liga u e v ou None se não forem adjacentes"""
        edge = self._vertices[u].get(v)  # returns None se não existir aresta alguma entre u e v
        if edge != None and self._directed:  # se é dirigido
            _, x = edge.endpoints  # vai confirmar se é u --> v
            if x != v:
                edge = None
        return edge

    def degree(self, v, outgoing=True):
        """quantidade de arestas incidentes no vértice v
        Se for um grafo dirigido, conta apenas as arestas outcoming ou em incoming, de acordo com o valor de outgoing
        """
        adj = self._vertices
        if not self._directed:
            count = len(adj[v])
        else:
            count = 0
            for edge in adj[v].values():
                x, y = edge.endpoints()
                if (outgoing and x == v) or (not outgoing and y == v):
                    count += 1
        return count

    def remove_edge(self, u, v):
        """Remove a aresta entre u e v """
        if u in self._vertices.keys() and v in self._vertices[u].keys():
            del self._vertices[u][v]
            del self._vertices[v][u]

    def remove_vertex(self, v):
        """remove o vértice v"""
        # remover todas as arestas de [v]
        # remover todas as arestas com v noutros vertices
        # remover o vértice
        if v in self._vertices.keys():
            lst = [i for i in self.incident_edges(v)]
            for i in lst:
                x, y = i.endpoints()
                self.remove_edge(x, y)
            del self._vertices[v]
        # return v

"""2. Método de carregamento de dados de um ficheiro csv"""
def read_csv():
    """TODO: A implementar"""
    filename = ""
    with open(filename, 'r') as file:
        data = csv.DictReader(file, delimiter=",")
        for row in data:
            print(row)

""" 3. Proceda ao Carregamento de dados do ficheiro Github.csv (no e-Learning)"""
def github_csv():
    """TODO: A implementar"""
    info = []
    filename = "Github1.csv"
    with open(filename, 'r') as file:
        data = csv.DictReader(file, delimiter=",")
        for row in data:
            first_col = row["follower"]
            second_col = row["followed"]
            object = Edge(first_col, second_col)
            info.append(object)
    return info


