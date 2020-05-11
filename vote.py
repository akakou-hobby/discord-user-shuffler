import random
import copy


class ScoreCalculator:
    def __init__(self, elements):
        self.elements = copy.copy(elements)
        self.results = []

        for element in elements:
            self.results.append([element, 0])
    
    def calc(self, answers, correct_answer):
        for user, target in answers:
            for index, value in enumerate(self.results):
                if value[0] == target:
                    if target == correct_answer:
                        self.results[index][1] += 1.5
                    else:
                        self.results[index][1] += 1

                if target == correct_answer and value[0] == user:
                    self.results[index][1] += len(self.elements) / 2

        self.results.sort(key=lambda x: x[1])
        self.results.reverse()

        return self.results
    
if __name__=='__main__':
    elements = ['1', '2', '3', '4', '5']
    answers = [('1', '2'), ('3', '2'), ('5', '3')]

    v = ScoreCalculator(elements)
    print(v.calc(answers, '3'))
