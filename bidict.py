
class Empty:
    pass


class BaseBiDict(object):

    __SIZE = 10

    def __init__(self):
        self.container_a = [None] * self.__SIZE
        self.container_b = [None] * self.__SIZE

    def _generate_index(self, data):
        return sum(ord(c) for c in str(data)) % self.__SIZE

    def _get_node(self, container, data):
        idx = self._generate_index(data)
        node = container[idx]
        while node is not None and node.data != data:
            node = node.next
        return node

    def _set_node(self, container, node):
        idx = self._generate_index(node.data)
        if container[idx] is None:
            container[idx] = node
        else:
            current_node = container[idx]
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = node

    def _delete_node(self, container, node):
        if node.prev is None:
            idx = self._generate_index(node.data)
            container[idx] = None
        else:
            if node.next is not None:
                node.next.prev = node.prev
            node.prev.next = node.next

    def _get(self, container, data, default=Empty, raise_exception=True):
        node = self._get_node(container, data)
        if node is None:
            if raise_exception or default != Empty:
                raise KeyError(f"'{data}'")
            return default
        return self._extract_peer_data(node)

    def get_a(self, data, **kwargs):
        return self._get(self.container_a, data, **kwargs)

    def get_b(self, data):
        return self._get(self.container_b, data, **kwargs)

    def _extract_peer_data(self, node):
        raise NotImplementedError

    def _str(self, container):
        strings = []
        for node in container:
            while node is not None:
                peer_data = self._extract_peer_data(node)
                strings.append(f"{node.data} <-> {peer_data}")
                node = node.next
        return strings

    def __str__(self):
        a_head = ['', '### A ###', '']
        b_head = ['', '### B ###', '']
        return '\n'.join(
            a_head + self._str(self.container_a) + b_head + self._str(self.container_b)
        )


class BiDictNode(object):

    def __init__(self, data):
        self.data = data
        self.peer = None
        self.next = None
        self.prev = None


class BiDict(BaseBiDict):

    def _extract_peer_data(self, node):
        return node.peer.data

    def del_a(self, data):
        node = self._get_node(self.container_a, data)
        if node is not None:
            self._delete_node(self.container_a, node)
            self._delete_node(self.container_b, node.peer)

    def del_b(self, data):
        node = self._get_node(self.container_b, data)
        if node is not None:
            self._delete_node(self.container_b, node)
            self._delete_node(self.container_a, node.peer)

    def set(self, data_a, data_b):
        self.del_a(data_a)
        self.del_b(data_b)
        node_a = BiDictNode(data_a)
        node_b = BiDictNode(data_b)
        node_a.peer = node_b
        node_b.peer = node_a
        self._set_node(self.container_a, node_a)
        self._set_node(self.container_b, node_b)


class MultiBiDictNode(object):

    def __init__(self, data):
        self.data = data
        self.peers = []
        self.next = None
        self.prev = None


class MultiBiDict(BaseBiDict):

    def _extract_peer_data(self, node):
        return [peer.data for peer in node.peers]

    def _get_or_set_node(self, container, data):
        node = self._get_node(container, data)
        if node is not None:
            return node
        node = MultiBiDictNode(data)
        self._set_node(container, node)
        return node

    def add(self, data_a, data_b):
        node_a = self._get_or_set_node(self.container_a, data_a)
        node_b = self._get_or_set_node(self.container_b, data_b)
        node_a.peers.append(node_b)
        node_b.peers.append(node_a)

    def remove(self, data_a, data_b):

        node_a = self._get_node(self.container_a, data_a)
        node_b = self._get_node(self.container_b, data_b)

        if node_a is None or node_b is None:
            return print(f"node_a: {node_a} node_b: {node_b}")

        # python list.remove deletes item only if the match is exact
        node_a.peers.remove(node_b)
        node_b.peers.remove(node_a)

        if not node_a.peers:
            self._delete_node(self.container_a, node_a)
        if not node_b.peers:
            self._delete_node(self.container_b, node_b)

# import importlib; import bidict; importlib.reload(bidict); d = bidict.MultiBiDict(); d.add('six', 'kuusi'); d.add('spruce', 'kuusi'); print(d)
