# ISCTE-IUL
# 1º ano - Licenciatura em Ciência de Dados
# Projeto Final - U.C Estruturas de Dados e Algoritmos
# Grupo: João Portásio nº 94754 | Sandra Silva nº 98372 | Tiago Madeira nº 95088
#
# -------------------------------------------------- #

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


class Edge:
    """Estrutura de Aresta para um Grafo: (origem, destino) e seu peso """

    def __init__(self, u, v, p):
        self._origin = u
        self._destination = v
        self._weight = p

    def __hash__(self):
        # para associar a aresta a uma chave para um dicionário
        return hash((self._origin, self._destination))

    def __str__(self):
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
