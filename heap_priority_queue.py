
"""
Implementação efetuada de acordo com a bibliografia:

Data Structures and Algorithms in Python

"""

class PriorityQueueBase:
    """Classe base abstrata para uma fila prioritária"""
    class _Item:
        __slots__ = '_key', '_value'

        def __init__(self, key, value):
            self._key = key
            self._value = value

        @property
        def key(self):
            return self._key

        @property
        def value(self):
            return self._value

        def __lt__(self, other):
            return self._key < other.key     # comparar itens com base nas suas chaves

    def is_empty(self):
        """Retorna TRUE se a fila prioritária estiver vazia."""
        return len(self) == 0


class HeapPriorityQueue(PriorityQueueBase):
    # ------------------------------ nonpublic behaviors ------------------------------
    def _parent(self, j):
        return (j-1) // 2

    def _left(self, j):
        return 2*j + 1

    def _right(self, j):
        return 2*j + 2

    def _has_left(self, j):
        return self._left(j) < len(self._data)

    def _has_right(self, j):
        return self._right(j) < len(self._data)

    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    def _upheap(self, j):
        parent = self._parent(j)
        if j > 0 and self._data[j] < self._data[parent]:
            self._swap(j, parent)
            self._upheap(parent)

    def _downheap(self, j):
        if self._has_left(j):
            left = self._left(j)
            small_child = left
            if self._has_right(j):
                right = self._right(j)
                if self._data[right] < self._data[left]:
                    small_child = right
            if self._data[small_child] < self._data[j]:
                self._swap(j, small_child)
                self._downheap(small_child)

    # ------------------------------ public behaviors ------------------------------

    def __init__(self):
        """Cria uma nova fila prioritária vazia."""
        self._data = []

    def __len__(self):
        """Devolve o número de items na fila prioritária."""
        return len(self._data)

    def add(self, key, value):
        """Adiciona um par de key: value à fila prioritária"""
        self._data.append(self._Item(key, value))
        self._upheap(len(self._data)-1)

    def min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty!')
        item = self._data[0]
        return item._key, item._value

    def remove_min(self):
        if self.is_empty():
            raise Empty('Priority queue is empty!')
        self._swap(0, len(self._data)-1)
        item = self._data.pop()
        self._downheap(0)
        return item._key, item._value


class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    """Uma fila prioritária baseada em localizadores implementada com uma pilha binária."""

    # ------------------------------ nested Locator class ------------------------------
    class Locator(HeapPriorityQueue._Item):
        """Token para localizar uma entrada da fila prioritária"""
        __slots__ = '_index'

        def __init__(self, k, v, j):
            super().__init__(k, v)
            self._index = j

    # ------------------------------ nonpublic behaviors ------------------------------
    # substituição do swap para registar novos índices
    def _swap(self, i, j):
        super()._swap(i, j)             # faz a troca
        self._data[i]._index = i        # reinicia o índice de localização (pós-troca)
        self._data[j]._index = j        # reinicia o índice de localização (pós-troca)

    def _bubble(self, j):
        if j > 0 and self._data[j] < self._data[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)

    def add(self, key, value):
        """Adiciona um par key: value"""
        token = self.Locator(key, value, len(self._data))
        self._data.append(token)
        self._upheap(len(self._data)-1)
        return token

    def update(self, loc, newkey, newval):
        """Actualiza a chave e o valor para a entrada identificada pelo Locator loc."""
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        loc._key = newkey
        loc._value = newval
        self._bubble(j)

    def remove(self, loc):
        """Remove e devolve o par (k, v) identificado pelo Locator loc."""
        j = loc._index
        if not (0 <= j < len(self) and self._data[j] is loc):
            raise ValueError('Invalid locator')
        if j == len(self) - 1:      # item na última posição
            self._data.pop()        # remove o item na última posição
        else:
            self._swap(j, len(self)-1)      # troca o item para a última posição
            self._data.pop()                # remove o item da lista
            self._bubble(j)                 # ajusta o item desorganizado pela troca efetuada
        return loc._key, loc._value