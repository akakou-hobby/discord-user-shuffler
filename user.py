class GameUser:
    def __init__(self, member):
        self.member = member
        self.channel = None
        self.vote = None
        self.spoofed = None
        self.is_answer = False
        self.score = 0

class GameUserRepository():
    users = []

    def add(self, user):
        self.users.append(user)
    
    def update(self, user):
        for index, _user in enumerate(self.users):
            if _user.member == user.member:
                self.users[index] = user

    def get(self, name='', member=None, channel=None, vote=None, spoofed=None, is_answer=False):
        for user in self.users:
            if name and user.member.name != name:
                continue

            if member and user.member != member:
                continue

            if channel and user.channel != channel:
                continue

            if vote and user.vote != vote:
                continue

            if spoofed and user.spoofed != spoofed:
                continue

            if is_answer and not user.is_answer:
                continue

            return user
        
        return None
