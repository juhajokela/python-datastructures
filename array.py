class Array(list):

    def __init__(self, *values):
        super().__init__(values)

    def map(self, function):
        return Array(*[function(x) for x in self])

    def filter(self, function):
        return Array(*[x for x in self if function(x)])

    def __repr__(self):
        string = super().__repr__()
        return f"Array({string[1:-1]})"
