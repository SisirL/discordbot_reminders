import discord
def set_up_intents():
    intents = discord.Intents.default()
    intents.typing = False
    intents.presences = False
    intents.members = True
    intents.message_content = True

    return intents

def get_discord_token() -> str:
    with open("offline_details.txt", 'r') as file:
        token = file.readlines()[0].strip()
    return token

def get_gemini_key() -> str:
    with open("offline_details.txt", 'r') as file:
        api_key = file.readlines()[1].strip()
    return api_key
