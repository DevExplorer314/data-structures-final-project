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

    def __init__(self, directed=False):
        """
        Cria um grafo vazio (por omissão será não dirigido e usa o contentor vertices)
        O Grafo é orientado se o parâmetro directed tiver o valor True
        """
        self._outgoing = {}
        # o dicionário seguinte apenas é criado se o grafo for orientado; senão usa-se um alias para o 1o.
        self._incoming = {} if directed else self._outgoing

    def is_directed(self):
        """com base na criação original da instância, devolve True se o Grafo é dirigido; False senão """
        return self._incoming is not self._outgoing  # True se os dois contentores são distintos

    def vertex_count(self):
        """Devolve a quantidade de vértices no grafo"""
        return len(self._outgoing)

    def vertices(self):
        """Devolve um iterador de todos os vértices do Grafo"""
        return self._outgoing.keys()

    def edge_count(self):
        """Devolve a quantidade de arestas do Grafo"""
        # soma as arestas em outgoing para cada vértice
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # se é não orientado, há duplicação de arestas em cada vértice extremo
        return total if self.is_directed() else total // 2

    def edges(self):
        """Devolve o conjunto de todas as arestas do Grafo"""
        result = set()  # set pois, se é não orientado, há duplicação de arestas em cada vértice extremo
        # pelo que deve guardar apenas uma ocorrência de cada uma
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """Devolve a aresta que liga u e v (ou None se não forem adjacentes)"""
        return self._outgoing[u].get(v)  # get devolve None se não encontrar

    def degree(self, v, outgoing=True):
        """
        Quantidade de arestas (em outgoing) incidentes no vértice v
        Se for um grafo dirigido, e outgoing for False, conta as arestas em incoming
        """
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """
        Devolve todas as arestas (outgoing) incidentes em v
        Se for um grafo dirigido, e outgoing for False, conta as arestas em incoming
        """
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, v):
        """Insere e devolve um novo vértice com o elemento x"""
        self._outgoing[v] = {}
        if self.is_directed():
            # se dirigido, precisa ainda da "lista" de vértices a chegar
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """Insere e devolve uma nova aresta entre u e v com peso x"""
        e = Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    def remove_edge(self, u, v):
        """Remove a aresta entre u e v """
        del self._outgoing[u][v]
        del self._incoming[v][u]

    def remove_vertex(self, v):
        """remove o vértice v"""
        # remover todas as arestas de outgoing [v]
        # remover todas as arestas de incoming [v]
        # remover o vértice de x
        for i in self.incident_edges(v):
            self.remove_edge(v, i)
        del self._outgoing[v]
        if self.is_directed():
            for i in self.incident_edges(v, False):
                self.remove_edge(i, v)
            del self._incoming[v]
        return v

"""2. Método de carregamento de dados de um ficheiro csv que obedeça ao seguinte formato:
    i) por linha existem 3 valores de dados - o 1.º e o 2.º indicam nomes de vértices e o 3.º um peso. 
    ii) A 1.ª linha do ficheiro indica o nome das colunas.
    Nota importante: caso não exista 3ª coluna, devem assumir que o grafo não é pesado e lidar com essa situação sem erro
"""
def read_csv():
    """TODO: Dúvida colocada ao professor. A aguardar resposta"""
    with open('Github1.csv', newline='') as csv_file:    # abrir o ficheiro CSV
        reader = csv.reader(csv_file, delimiter=",")    # ler os dados no ficheiro CSV
        next(reader)        # ignora a primeira linha do ficheiro (nome das colunas)
        for row in reader:
            print(row)

""" 3. Proceda ao Carregamento de dados do ficheiro Github.csv (no e-Learning) """
def github_csv():
    data = []
    with open('Github1.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            object = Edge(row["follower"], row["followed"])
            data.append(object)
    return data

""" 5. Implementação de métodos para determinar caminhos mais curtos num grafo """

"""(a) sem usar os pesos nas arestas)"""
def shortest_path(graph, start, goal):
    explored = []

    # Queue for traversing the
    # graph in the BFS
    queue = [[start]]

    # If the desired node is
    # reached
    if start == goal:
        print("Same Node")
        return

    # Loop to traverse the graph
    # with the help of the queue
    while queue:
        path = queue.pop(0)
        node = path[-1]

        # Condition to check if the
        # current node is not visited
        if node not in explored:
            neighbours = graph[node]

            # Loop to iterate over the
            # neighbours of the node
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)

                # Condition to check if the
                # neighbour node is the goal
                if neighbour == goal:
                    print("Shortest path = ", *new_path)
                    return
            explored.append(node)

    # Condition when the nodes
    # are not connected
    print("So sorry, but a connecting" \
          "path doesn't exist :(")
    return


""" (b) usando os pesos nas arestas"""
def shortest_path_weight():
    '''TODO: Implementar o método utilizado no link abaixo.
    Link: https://www.youtube.com/watch?v=Ub4-nG09PFw
    '''
    pass

if __name__ == "__main__":

    g = Graph()

    ## Inserção de vértices
    g.insert_vertex('a')
    g.insert_vertex('b')
    g.insert_vertex('c')
    g.insert_vertex('d')
    g.insert_vertex('e')
    g.insert_vertex('f')

    ## Inserção de arestas
    g.insert_edge('a', 'b', 7)
    g.insert_edge('a', 'c', 9)
    g.insert_edge('a', 'f', 14)
    g.insert_edge('b', 'c', 10)
    g.insert_edge('b', 'd', 15)
    g.insert_edge('c', 'd', 11)
    g.insert_edge('c', 'f', 2)
    g.insert_edge('d', 'e', 6)
    g.insert_edge('e', 'f', 9)

    ## Grafo usando dicionários
    graph = {'A': ['B', 'E', 'C'],
             'B': ['A', 'D', 'E'],
             'C': ['A', 'F', 'G'],
             'D': ['B', 'E'],
             'E': ['A', 'B', 'D'],
             'F': ['C'],
             'G': ['C']}

    ## Shortest path sem usar os pesos nas arestas
    shortest_path(graph, 'A', 'D')
    shortest_path(graph, 'A', 'G')

    ## Shortest path usando os pesos nas arestas
