class Map(dict):

    def map(self, function):
        return Map({function(k, v) for k, v in self.items()})

    def filter(self, function):
        return Map({k: v for k, v in self.items() if function(k, v)})

    def __repr__(self):
        string = super().__repr__()
        return f"Map({string[1:-1]})"
