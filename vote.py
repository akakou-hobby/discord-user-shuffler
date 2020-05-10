import random
import copy


class VoteCompiler:
    def __init__(self, elements=[]):
        self.elements = copy.copy(elements)
        self.results = []

        for element in elements:
            self.results.append([element, 0])
    
    def compile(self, votes):
        for _, target in votes:
            for index, value in enumerate(self.results):
                if value[0] == target:
                    self.results[index][1] += 1
        
        return self.results
    


if __name__=='__main__':
    elements = ['1', '2', '3', '4', '5']
    votes = [('1', '2'), ('3', '2'), ('5', '3')]

    v = VoteCompiler(elements)
    print(v.compile(votes))
