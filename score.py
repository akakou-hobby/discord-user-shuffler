import random
import copy


class ScoreCalculator:
    def __init__(self, user_repo):
        self.user_repo = user_repo
        self.results = []

    def calc(self):
        for user in self.user_repo.users:
            self.user_repo.update(user)
            vote_user = self.user_repo.get(member=user.vote)

            if vote_user.is_answer:
                user.score += 1
                vote_user.score += 1.5
            else:
                vote_user.score += 1

            self.user_repo.update(vote_user)

        self.result = sorted(self.user_repo.users, key=lambda x: x.score)[::-1]
        return self.result
