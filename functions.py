import discord
import config
import time
import ai_chatter
import warnings
warnings.filterwarnings("ignore", "Runtime warning received", RuntimeWarning)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Login as {self.user} successful (ID: {self.user.id})')
        ai_chatter.connect_gemini()
        ai_chatter.gemini_setup()
    
    async def on_message(self, message: discord.Message):
        def time_delay(func):
            async def inner(seconds, message: discord.Message):
                time.sleep(seconds)
                await func(seconds, message)
            return inner
        @time_delay
        async def remind_after(seconds: int, message: discord.Message):
            await message.reply("Your time is over!", mention_author=True)
        
        if message.author.id == self.user.id:
            return
        if message.content.strip().startswith("!hello"):
            await message.reply("Hello!", mention_author=True)
        elif message.content.strip().startswith("!remind"):
            info = message.content[8:].strip()
            seconds = 0
            try:
                duration = [x.strip() for x in info.split()]
                if 'd' in info:
                    days = int([x.strip()[:-1] for x in duration if 'd' in x][0])
                    seconds += 86400*days
                if 'h' in info:
                    hours = int([x.strip()[:-1] for x in duration if 'h' in x][0])
                    seconds += 3600*days
                if 'm' in info:
                    minutes = int([x.strip()[:-1] for x in duration if 'm' in x][0])
                    seconds += 60*minutes
                if 's' in info:
                    seconds += int([x.strip()[:-1] for x in duration if 's' in x][0])
                if not seconds:
                    await message.reply("Please specify the time correctly.")
                else:
                    await message.reply("Okay, I will remind you!")
                    await remind_after(seconds, message)
            except Exception as e:
                print(e.with_traceback())

        else:
            reponse = ai_chatter.get_response(message.content.strip())
            await message.reply(reponse, mention_author=True)
            # await message.reply from gemini

        '''
        Message:
          id: int/long
          channel: TextChannel
            id: int/long (link)
            name: str (#)
            position: int/bool
            nsfw: bool
            news: bool
            category_id: int/long
          type: MessageType.default: int/bool
          author: Member
            id: int/long
            name: str (username)
            global_name: str|None
            bot: bool
            nick: str|None
            guild: Guild
              id: int/long (link)
              name: str
              shard_id: int/bool
              chunked: bool
              member_count: int (incl self)
          flags: MessageFlags
            value: int
        '''

intents = config.set_up_intents()
token = config.get_discord_token()
google_key = config.get_gemini_key()
client = MyClient(intents=intents)
client.run(token=token)    # token
"# discordbot_reminders" 
