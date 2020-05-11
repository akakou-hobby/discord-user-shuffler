import random
import copy

from user import GameUser

class PairShuffler:
    def __init__(self, elements=[]):
        self.elements = copy.copy(elements)
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

        element = random.choice(self.elements)
        self.elements.remove(element)

        while has_inviled_pair:
            self.shuffle_without_check()
            has_inviled_pair = self.has_inviled_pair()
        
        self.pairs.append((element, element))

        return self.pairs, element

class UserPairShaffler:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        altenatives = list(range(len(user_repo.users)))
        self.shuffler = PairShuffler(altenatives)
    
    def shuffle(self):
        pairs, _ = self.shuffler.shuffle()

        for pair in pairs:
            user_index = pair[0]
            user = self.user_repo.users[user_index]

            spoofed_index = pair[1]
            spoofed = self.user_repo.users[spoofed_index].member

            if user.member == spoofed:
                user.is_answer = True
            
            user.spoofed = spoofed
            self.user_repo.update(user)



if __name__=='__main__':
    elements = ['1', '2', '3', '4', '5']
    shuffler = PairShuffler(elements)

    pairs = shuffler.shuffle()

    for pair in pairs:
        print(pair)