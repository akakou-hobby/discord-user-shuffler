import random
import copy


class PairShuffler:
    def __init__(self, elements=[]):
        self.elements = elements
        self.pairs = []

    def shuffle_without_check(self):
        self.pairs = []
        
        shuffled_elements = copy.copy(self.elements)
        random.shuffle(shuffled_elements)

        for first, second in zip(self.elements, shuffled_elements):
            pair = (first, second)
            self.pairs.append(pair)

        return self.pairs
    
    def has_inviled_pair(self):
        for first, second in self.pairs:
            if first == second:
                return True

        return False

    def shuffle(self):
        has_inviled_pair = True

        while has_inviled_pair:
            self.shuffle_without_check()
            has_inviled_pair = self.has_inviled_pair()

        return self.pairs

if __name__=='__main__':
    elements = ['1', '2', '3', '4', '5']
    shuffler = PairShuffler(elements)

    pairs = shuffler.shuffle()

    for pair in pairs:
        print(pair)