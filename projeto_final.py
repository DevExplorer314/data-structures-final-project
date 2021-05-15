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

    __slots__ = "_element", "neighbors"

    def __init__(self, x):
        """O vértice será inserido no Grafo usando o método insert_vertex(x) que cria um Vertex"""
        self._element = x
        self.neighbors = list()

    def vertice(self):
        """Devolve o nome deste vértice; esconde o verdadeiro identificador do atributo"""
        return self._element

    def add_neighbor(self, v):
        if v not in self.neighbors:
            self.neighbors.append(v)
            self.neighbors.sort()

    """Comparação de vértices"""

    def __eq__(self, other):
        if isinstance(other, Vertex):
            return self._element == other.vertice()
        return False

    def __repr__(self):
        return '{0}'.format(self._element)

    def __hash__(self):
        """Referência de memória (usada por causa das keys dos dicionários)"""
        return hash(id(self))  # devolve um inteiro que identifica este vértice como uma chave num dicionário


# == Class Edge == #
class Edge:
    """Estrutura de Aresta para um Grafo: (origem, destino) e seu peso """

    __slots__ = '_origin', '_destination', '_weight'

    def __init__(self, u, v, p=None):
        self._origin = u
        self._destination = v
        self._weight = p

    def __hash__(self):
        # para associar a aresta a uma chave para um dicionário
        return hash((self._origin, self._destination))

    def __repr__(self):
        if self._weight is None:
            return '({0}, {1})'.format(self._origin, self._destination)
        return '({0}, {1}, {2})'.format(self._origin, self._destination, self._weight)

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
    '''Representação de um grafo usando mapeamentos de adjacências (associações) com dictionaries'''

    def __init__(self, directed=False):
        '''Cria um grafo vazio (dicionário de _vertices); é orientado se o parâmetro directed tiver o valor True'''
        self._directed = directed
        self._number = 0            # quantidade de nós no Grafo
        self._vertices = {}         # dicionário com chave vértice e valor dicionário de adjacências

    def __getitem__(self, arg):
        return self._vertices[arg]

    def insert_vertex(self, x):
        '''Insere e devolve um novo vértice com o elemento x'''
        v = Vertex(x)
        self._vertices[v] = {}      # inicializa o dicionário de adjacências a vazio
        self._number = len(self._vertices)
        return v

    def insert_edge(self, u, v, x=None):
        '''Cria u e v e insere e devolve uma nova aresta entre u e v com peso x'''
        e = Edge(u, v, x)
        self._vertices[u][v] = e  # vai colocar nas adjacências de u
        self._vertices[v][u] = e  # e nas adjacências de v (para facilitar a procura de todos os arcos incidentes)

    def incident_edges(self, v, outgoing=True):
        '''Gerador: indica todas as arestas (outgoing) incidentes em v
           Se for um grafo dirigido e outgoing for False, devolve as arestas em incoming
        '''
        for edge in self._vertices[v].values(): # para todas as arestas relativas a v:
            if not self._directed:
                    yield edge
            else:  # senão deve ir procurar em todas as arestas para saber quais entram ou saiem
                x, y = edge.endpoints()
                if (outgoing and x == v) or (not outgoing and y == v):
                    yield edge

    def is_directed(self):
        '''com base na criação original da instância, devolve True se o Grafo é dirigido; False senão '''
        return self._directed  # True se os dois contentores são distintos

    def vertex_count(self):
        '''Devolve a quantidade de vértices no grafo'''
        return self._number

    def vertices(self):
        '''Devolve um iterável sobre todos os vértices do Grafo'''
        return self._vertices.keys()

    def edge_count(self):
        '''Devolve a quantidade de arestas do Grafo'''
        total = sum(len(self._vertices[v]) for v in self._vertices)
        # for undirected graphs, make sure not to double-count edges
        return total if self._directed else total // 2

    def edges(self):
        '''Devolve o conjunto de todas as arestas do Grafo'''
        result = set()      # avoid double-reporting edges in undirected graph
        for secondary_map in self._vertices.values():
            result.update(secondary_map.values())  # add edges to resulting set
        return result

    def get_edge(self, u, v):
        '''Devolve a aresta que liga u e v ou None se não forem adjacentes'''
        edge = self._vertices[u].get(v) # returns None se não existir aresta alguma entre u e v
        if edge != None and self._directed: # se é dirigido
            _, x = edge.endpoints           # vai confirmar se é u --> v
            if x != v:
                edge = None
        return edge

    def degree(self, v, outgoing=True):
        '''quantidade de arestas incidentes no vértice v
        Se for um grafo dirigido, conta apenas as arestas outcoming ou em incoming, de acordo com o valor de outgoing
        '''
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
        '''Remove a aresta entre u e v '''
        if  u in self._vertices.keys() and v in self._vertices[u].keys():
            del self._vertices[u][v]
            del self._vertices[v][u]

    def remove_vertex(self, v):
        '''remove o vértice v'''
        # remover todas as arestas de [v]
        # remover todas as arestas com v noutros vertices
        # remover o vértice
        if v in self._vertices.keys():
            lst = [i for i in self.incident_edges(v)]
            for i in lst:
                x, y = i.endpoints()
                self.remove_edge(x,y)
            del self._vertices[v]
        #return v

    def printG(self):
        '''Mostra o grafo por linhas'''
        print('Grafo Orientado:', self.is_directed())

        '''Mostra o número de vertices'''
        print("Número de Vertices: {}".format(graph.vertex_count()))

        '''Mostra o número de arestas'''
        print("Número de Arestas: {}".format(graph.edge_count()))

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
    info = []
    with open(filename, 'r') as csv_file:
        data = csv.reader(csv_file)
        next(data)

        for linha in data:
            id_origem = linha[0]
            id_destino = linha[1]
            peso = linha[2] if len(linha) > 2 else 1 # None
            info.append([id_origem, id_destino, peso])

    return info

def build_graph():

    csv_data = read_csv(filename)
    graph = Graph()

    for linha in csv_data:
        id_origem = linha[0]
        id_destino = linha[1]
        peso = linha[2] if len(linha) > 2 else 1  # None

        v_origem = graph.insert_vertex(id_origem)
        v_destino = graph.insert_vertex(id_destino)

        graph.insert_edge(v_origem, v_destino, peso)

    return graph


""" 5. Implementação de métodos para determinar caminhos mais curtos num grafo """

"""(a) sem usar os pesos nas arestas)"""

""" (b) usando os pesos nas arestas"""


if __name__ == "__main__":

    # Ficheiro CSV a ler
    filename = "Data_Facebook_TESTE.csv"

    # Criação do grafo
    graph = build_graph()

    # Print do grafo
    #graph.printG()

    #shortest_path(graph, "Murray", "Douglas")


    ## Teste do caminho mais curto sem usar os pesos nas arestas
    #print("=== Sem usar os pesos nas arestas === ")
    #shortest_path(graph, "Murray", "Ryan")

    ## Teste do caminho mais curto usando os pesos nas arestas
    #print("=== Usando os pesos nas arestas ===")
    #dijkstra(graph, "Murray", "Ryan")
