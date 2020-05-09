class STATUS:
    STARTING = 'starting'
    RUNNING = 'runnning'


class DiscordShuffleGame:
    def __init__(self):
        self.users = []
        self.status = STATUS.STARTING

    async def ready(self, channel):
        self.channel = channel
        await channel.send('Botが起動しました。\nゲームに参加するには、「参加」と送信して下さい。\nまたゲームを開始するには、「開始」と送信して下さい。')

    async def start(self, message):
        if message.content == '参加':
            user = message.author

            if user not in self.users:
                self.users.append(user)
                await self.channel.send(f'{user.name}さんを追加しました。')
            else:
                await self.channel.send(f'{user.name}さんは既に参加しています。')

        elif message.content == '開始':
            self.status = STATUS.RUNNING
            
            print(self.users)
            await self.channel.send(f'開始します。')
        
    async def next(self, message):
        if self.status == STATUS.STARTING:
            await self.start(message)
        
