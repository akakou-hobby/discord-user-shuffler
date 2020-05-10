from shuffle import PairShuffler
import discord

import sys


class STATUS:
    READYING = 'starting'
    SPOOFING = 'spoofing'
    VOTING = 'voting'

class GameState:
    def __init__(self):
        self.users = []
        self.status = STATUS.READYING
        
        self.pairs = []
        self.channels = []
        self.votes = []
        self.main_channel = None
        self.client = None

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
            channel_name = f'shuffler-{user}'
            
            def search_channel(c):
                result = c.name == channel_name.replace('#', '')
                return result

            channel = next(filter(search_channel, guild.channels), None)

            if not channel:
                role = await guild.create_role(name=channel_name)
                await user.add_roles(role)

                overwrites = {
                    role: discord.PermissionOverwrite(read_messages=True),
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                
                channel = await guild.create_text_channel(channel_name, type=discord.ChannelType.text, overwrites=overwrites)
            
            state.channels.append(channel)
            await channel.send(f'あなたがなりすます対象は、{target.name}です。\nなりすます際は、このチャンネルにメッセージを送信して下さい。')
        
        await state.main_channel.send(f'議論が終わり次第、「投票」を送信して下さい。')
        state.status = STATUS.SPOOFING
    
class GameSpoofPhase(GamePhase):
    def __init__(self):
        super().__init__()
    
    async def run(self, message):
        if message.channel == state.main_channel and message.content == '投票':
            await state.main_channel.send(f'議論を終了しました。\n投票に入ります。')
            
            for channel in state.channels:
                await channel.send('本人だと思う人の名前を送信して下さい。\n\n選択肢：')

                for user in state.users:
                    await channel.send(f'「{user.name}」')
            
            state.status = STATUS.VOTING
            
        elif message.channel in state.channels:
            filtered_pair = filter(lambda pair: pair[0] == message.author, state.pairs)
            _, target = next(filtered_pair)
            await state.main_channel.send(f'{target.name}\n> {message.content}')

class GameVotePhase(GamePhase):
    def __init__(self):
        super().__init__()
    
    async def run(self, message):        
        if message.channel not in state.channels:
            return
        
        if next(filter(lambda vote: message.author == vote[0], state.votes), None):
            await message.channel.send('既に投票されています。')
            return

        user = next(filter(lambda user: message.content == user.name, state.users), None)
        state.votes.append((message.author, user))
        await message.channel.send('投票しました。')


        if len(state.votes) == len(state.users):
            await state.main_channel.send('投票が終了しました。')


class Game:
    def __init__(self):
        self.ready = GameReadyPhase()
        self.spoof = GameSpoofPhase()
        self.vote = GameVotePhase()

    async def setup(self, channel, client):
        state.main_channel = channel
        state.client = client
        await channel.send('Botが起動しました。\nゲームに参加するには、「参加」と送信して下さい。\nまたゲームを開始するには、「開始」と送信して下さい。')

    async def next(self, message):
        if state.status == STATUS.READYING:
            await self.ready.run(message)
        elif state.status == STATUS.SPOOFING:
            await self.spoof.run(message)
        elif state.status == STATUS.VOTING:
            await self.vote.run(message)