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

            shuffler = PairShuffler(self.users)
            self.pairs = shuffler.shuffle()
            
            print(self.pairs)

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
                await channel.send(f'あなたがなりすます対象は、{target.name}です。')
                await channel.send(f'なりすます際は、このチャンネルにメッセージを送信して下さい。')
        
    async def next(self, message):
        if self.status == STATUS.STARTING:
            await self.start(message)
        
