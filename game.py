from shuffle import PairShuffler
import discord

class STATUS:
    STARTING = 'starting'
    RUNNING = 'runnning'



class DiscordShuffleGame:
    def __init__(self):
        self.users = []
        self.status = STATUS.STARTING
        
        self.pairs = []
        self.channels = []

    async def ready(self, channel):
        self.main_channel = channel
        await channel.send('Botが起動しました。\nゲームに参加するには、「参加」と送信して下さい。\nまたゲームを開始するには、「開始」と送信して下さい。')

    async def start(self, message):
        if message.channel != self.main_channel:
            return

        if message.content == '参加':
            user = message.author

            if user not in self.users:
                self.users.append(user)
                await self.main_channel.send(f'{user.name}さんを追加しました。')
            else:
                await self.main_channel.send(f'{user.name}さんは既に参加しています。')

        elif message.content == '開始':
            self.status = STATUS.RUNNING
            await self.main_channel.send(f'開始します。')

            shuffler = PairShuffler(self.users)
            self.pairs = shuffler.shuffle()

            for user, target in self.pairs:
                guild = user.guild
                
                role = await guild.create_role(name=f'shuffler-{user}')
                await user.add_roles(role)

                overwrites = {
                    role: discord.PermissionOverwrite(read_messages=True),
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True)
                }
                
                channel = await guild.create_text_channel(f'shuffler-{user}', type=discord.ChannelType.text, overwrites=overwrites)
                self.channels.append(channel)

                await channel.send(f'あなたがなりすます対象は、{target.name}です。')
                await channel.send(f'なりすます際は、このチャンネルにメッセージを送信して下さい。')
    
    async def run(self, message):
        if message.channel == self.main_channel and message.content == '終了':
            await self.main_channel.send(f'終了しました。\n\n結果')

            for user, target in self.pairs:
                await self.main_channel.send(f'{user} -> {target}')
                
        elif message.channel in self.channels:
            await self.main_channel.send(f'{message.author.name}\n{message.content}')
        

    async def next(self, message):
        if self.status == STATUS.STARTING:
            await self.start(message)
        
        if self.status == STATUS.RUNNING:
            await self.run(message)
