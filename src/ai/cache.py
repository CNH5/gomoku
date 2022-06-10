class Cache:
    def __init__(self):
        self._cache = {}

    def get(self, key):
        try:
            return self._cache[str(key)]
        except KeyError:
            return None

    def save(self, key, node):
        self._cache[str(key)] = node
