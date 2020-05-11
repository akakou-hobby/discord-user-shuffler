from shuffle import UserPairShaffler
from score import ScoreCalculator
from user import GameUser, GameUserRepository

import discord

import sys


class STATUS:
    READYING = 'starting'
    SPOOFING = 'spoofing'
    VOTING = 'voting'

class GameState:
    def __init__(self):
        self.user_repo = GameUserRepository()

        self.status = STATUS.READYING
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
        member = message.author

        if not state.user_repo.get(member=member):
            user = GameUser(member)
            state.user_repo.add(user)
            await state.main_channel.send(f'{member.name}さんを追加しました。')
        else:
            await state.main_channel.send(f'{member.name}さんは既に参加しています。')

    async def start(self, message):        
        await state.main_channel.send(f'開始します。')

        shuffler = UserPairShaffler(state.user_repo)
        shuffler.shuffle()

        for user in state.user_repo.users:
            guild = user.member.guild
            channel_name = f'shuffler-{user.member.name}'
  
            channel = next(filter(lambda channel: channel.name == channel_name, guild.channels), None)

            if not channel:
                role = await guild.create_role(name=channel_name)
                await user.member.add_roles(role)

                overwrites = {
                    role: discord.PermissionOverwrite(read_messages=True),
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                
                channel = await guild.create_text_channel(channel_name, type=discord.ChannelType.text, overwrites=overwrites)
            
            user.channel = channel
            state.user_repo.update(user)

            await channel.send(f'あなたがなりすます対象は、{user.spoofed.name}です。\nなりすます際は、このチャンネルにメッセージを送信して下さい。')
        
        await state.main_channel.send(f'議論が終わり次第、「投票」を送信して下さい。')
        state.status = STATUS.SPOOFING
    
class GameSpoofPhase(GamePhase):
    def __init__(self):
        super().__init__()
    
    async def run(self, message):
        user = state.user_repo.get(channel=message.channel)

        if message.channel == state.main_channel and message.content == '投票':
            await state.main_channel.send(f'議論を終了しました。\n投票に入ります。')
            
            for user in state.user_repo.users:
                if user.is_answer:
                    continue

                channel = user.channel
                await channel.send('本人だと思う人の名前を送信して下さい。\n\n選択肢：')

                for _user in state.user_repo.users:
                    if _user == user:
                        continue
                        
                    await channel.send(f'「{_user.member.name}」')
            
            state.status = STATUS.VOTING
            
        elif user:
            spoofed = user.spoofed
            await state.main_channel.send(f'{spoofed.name}\n> {message.content}')

class GameVotePhase(GamePhase):
    def __init__(self):
        super().__init__()
    
    async def run(self, message):        
        if not state.user_repo.get(channel=message.channel):
            return

        user = state.user_repo.get(member=message.author)

        if user.is_answer:
            await message.channel.send('答えとなる方に投票はできません。')
            return

        if user.vote:
            await message.channel.send('既に投票されています。')
            return


        vote_user = state.user_repo.get(name=message.content)
        if not vote_user:
            return

        if vote_user.member == user.member:
            await message.channel.send('自分に投票することはできません。')
            return

        user.vote = vote_user.member
        state.user_repo.update(user)

        await message.channel.send('投票しました。')

        vote_num = sum(bool(user.vote) for user in state.user_repo.users)

        if vote_num == len(state.user_repo.users) - 1:
            await state.main_channel.send('投票が終了しました。\n\n投票内容：')

            for user in state.user_repo.users:
                if not user.is_answer:
                    await state.main_channel.send(f'{user.member.name} -> {user.vote.name}')

            await state.main_channel.send('スコア：')

            calculator = ScoreCalculator(state.user_repo)
            results = calculator.calc()

            for index, user in enumerate(results):
                await state.main_channel.send(f'{index + 1}. {user.member.name}: {int(user.score)}')                 

            sys.exit()
            

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