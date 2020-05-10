from shuffle import PairShuffler
import discord

class STATUS:
    READYING = 'starting'
    RUNNING = 'runnning'

class GameState:
    def __init__(self):
        self.users = []
        self.status = STATUS.READYING
        
        self.pairs = []
        self.channels = []
        self.main_channel = None

state = GameState()

class GamePhase:
    def __init__(self):
        pass

    async def run(self, message):
        raise NotImplementedError

class GameReadyPhase(GamePhase):
    def __init__(self):
        super().__init__()

    async def run(self, message):
        if message.channel != state.main_channel:
            return

        if message.content == '参加':
            await self.join(message)

        elif message.content == '開始':
            await self.start(message)

    async def join(self, message):
        user = message.author

        if user not in state.users:
            state.users.append(user)
            await state.main_channel.send(f'{user.name}さんを追加しました。')
        else:
            await state.main_channel.send(f'{user.name}さんは既に参加しています。')

    async def start(self, message):        
        await state.main_channel.send(f'開始します。')

        shuffler = PairShuffler(state.users)
        state.pairs = shuffler.shuffle()

        for user, target in state.pairs:
            guild = user.guild
            
            role = await guild.create_role(name=f'shuffler-{user}')
            await user.add_roles(role)

            overwrites = {
                role: discord.PermissionOverwrite(read_messages=True),
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True)
            }
            
            channel = await guild.create_text_channel(f'shuffler-{user}', type=discord.ChannelType.text, overwrites=overwrites)
            state.channels.append(channel)

            await channel.send(f'あなたがなりすます対象は、{target.name}です。')
            await channel.send(f'なりすます際は、このチャンネルにメッセージを送信して下さい。')
        
        state.status = STATUS.RUNNING
    
class GameRunPhase(GamePhase):
    def __init__(self):
        super().__init__()
    
    async def run(self, message):
        if message.channel == state.main_channel and message.content == '終了':
            await state.main_channel.send(f'終了しました。\n\n結果')

            for user, target in state.pairs:
                await state.main_channel.send(f'{user} -> {target}')
                
        elif message.channel in state.channels:
            await state.main_channel.send(f'{message.author.name}\n{message.content}')

class Game:
    def __init__(self):
        self.ready = GameReadyPhase()
        self.run = GameRunPhase()

    async def setup(self, channel):
        state.main_channel = channel
        await channel.send('Botが起動しました。\nゲームに参加するには、「参加」と送信して下さい。\nまたゲームを開始するには、「開始」と送信して下さい。')

    async def next(self, message):
        if state.status == STATUS.READYING:
            await self.ready.run(message)
        elif state.status == STATUS.RUNNING:
            await self.run.run(message)
