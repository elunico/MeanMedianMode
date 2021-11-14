import functools

class ValueCount:
    def __init__(self, value, count):
        self.value = value 
        self.count = count 
    
    def __repr__(self):
        return 'ValueCount(value={}, count={})'.format(self.value, self.count)

    def __eq__(self, other):
        return self.value == other.value and self.count == other.count 

    def __hash__(self):
        return hash((self.value, self.count))
        

class MeanMedianMode:
    def __init__(self, iterable):
        self._data = iterable 
    
    @property 
    def data(self):
        return self._data 

    def update(self, *values):
        self._data.extend(values)
        self.mode.cache_clear()
        self.median.cache_clear()
        self.mean.cache_clear()
    
    def results(self):
        return self.mean(), self.median(), self.mode() 
    
    @functools.cache
    def mode(self):
        data = sorted([(i, self.data.count(i)) for i in self.data], key=lambda x: x[1], reverse=True)
        if len(data) == 0:
            return []
        
        first = data.pop(0)
        modals = set([ValueCount(first[0], first[1])])
        while data:
            n = data.pop(0)
            if first[1] != n[1]:
                return modals 
            modals.add(ValueCount(n[0], n[1]))
        return modals
    
    @functools.cache
    def median(self):
        self.data.sort()
        l = len(self.data)
        if l % 2 == 0:
            return (self.data[l // 2] + self.data[l // 2 + 1]) / 2 
        else:
            return self.data[l // 2]
    
    @functools.cache
    def mean(self):
        return sum(self.data) / len(self.data)

    def __repr__(self):
        return 'MeanMedianMode(data={})'.format(self.data)


print(MeanMedianMode(list(range(1,11)) + [1]).results())

a = MeanMedianMode([1,2,3])
print(a.results())
a.update(3, 4, 5)
print(a.results())