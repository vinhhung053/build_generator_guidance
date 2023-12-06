class ByteTrie(object):
    __slots__ = ('children', 'value', 'match_version', 'match', 'partial_match', 'parent', 'flag', 'log_prob')

    def __init__(self, byte_strings=None, values=None, parent=None):
        self.children = {}
        self.value = None
        self.match_version = -1
        self.match = False
        self.partial_match = False
        self.parent = parent
        self.flag = None # a spot for user code to store state
        self.log_prob = 0

        if byte_strings is not None:
            for i,s in enumerate(byte_strings):
                self.insert(s, None if values is None else values[i])

    def insert(self, s, value):
        if len(s) == 0:
            self.value = value
        else:
            first_byte = s[0:1]
            if first_byte not in self.children:
                self.children[first_byte] = ByteTrie(parent=self)
            self.children[first_byte].insert(s[1:], value)