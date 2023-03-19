import os
import time
import random
import discord
from discord import ui
from discord.ui import Select, View
from typing import List
from discord.ext import commands
from dotenv import load_dotenv

participant = []
option = []



class Card:
    card: List[int] = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
    card_word: List[str] = ['guard', 'priest', 'baron',
                            'handmaid', 'prince', 'king', 'countess', 'princess']
    card_num: int = 16

    def __init__(self):
        self.dump_pile: List[str] = []


class Player:

    def __init__(self, nickname, id):
        self.nickname = nickname
        self.id = id
        self.first_hand = "0"
        self.second_hand = "0"

class Game:
    start: bool = False

    def __init__(self, turns=0, guard_ability=0):
        self.turns = turns
        self.guard_ability = guard_ability
        self.winpoint = 0

class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or(
            '.'), intents=discord.Intents().all())

    async def on_ready(self):
        synced = await self.tree.sync()
        print("Slash CMDs Synced " + str(len(synced)) + " commands")

class SelectMenu(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder = "Choose your card", options=options)

    async def callback(self, interaction:discord.Interaction):
        values = ",".join(self.values)
        await interaction.response.edit_message(content = f"You have choose {values}")
        
    
class Select(discord.ui.View):
    def __init__(self, options):
        super().__init__()
        self.add_item(SelectMenu(options))

New_Game = Game()
Deck = Card()

class LeftButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=str(change_word(label)))

    async def callback(self, interaction: discord.Interaction):
        options = [
            discord.SelectOption(label= participant[0].nickname, value = participant[0].nickname),
            ]
        await interaction.response.edit_message(content = "Choose the player", view=Select(options))


class RightButton(discord.ui.Button):
    def __init__(self, label):
        super().__init__(label=str(change_word(label)))

    async def callback(self, interaction: discord.Interaction):
        options = [
            discord.SelectOption(label= participant[0].nickname, value = participant[0].nickname),
            ]
        await interaction.response.edit_message(content = "Choose the player", view=Select(options))


# player list method
def player_listing(participant):
    sentence = ''
    for player in participant:
        sentence += player.nickname
        sentence += ', '
    sentence += 'is in the game'
    return sentence


def change_word(num):
    if num == 1:
        return 'Guard `1`'
    elif num == 2:
        return 'Priest `2`'
    elif num == 3:
        return 'Baron `3`'
    elif num == 4:
        return 'Handmaid `4`'
    elif num == 5:
        return 'Prince `5`'
    elif num == 6:
        return 'King `6`'
    elif num == 7:
        return 'Countess `7`'
    elif num == 8:
        return 'Princess `8`'


def run_discord_bot():
    load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

    intents = discord.Intents.default()
    intents.message_content = True
    client = Client()

    participant_temp = []
    card_temp = []

    @client.tree.command(name="check", description="Command to check your cards")
    async def check(interaction: discord.Interaction):
        author = interaction.user.id
        for num in range(len(participant)):
            if author == participant[num].id:
                player = participant[num]
                first_hand = player.first_hand
                second_hand = player.second_hand
                if second_hand == "0":
                    await interaction.response.send_message("Your card is \"" + str(change_word(participant[num].first_hand)) + "\"", ephemeral=True)
                else:
                    await interaction.response.send_message(f"Your card are \"" + str(change_word(first_hand)) + "\",\"" + str(change_word(second_hand)) + "\"")

    @client.tree.command(name="action", description="Choose your card")
    async def action(interaction: discord.Interaction):
        author = interaction.user.id
        if participant[New_Game.turns].id == author:
            player = participant[New_Game.turns]
            first_hand = player.first_hand
            second_hand = player.second_hand
            left_button = LeftButton(first_hand)
            right_button = RightButton(second_hand)

            view = View()
            view.add_item(left_button)
            view.add_item(right_button)
            await interaction.response.send_message(content="Choose the card", view = view, ephemeral=True)
        else:
            await interaction.response.send_message("It is not your turn", ephemeral=True)

    @client.event
    async def on_message(message):
        if message.author == client.user:  # 디스코드 봇이 본인 메세지에 반응 방지
            return

        username: str = message.author  # 유저 이름
        user_message: str = message.content  # 유저 메세지
        channel: str = message.channel  # 체널 이름
        nickname_mention: str = message.author.name  # 유저 아이디(highlight)
        nickname: str = message.author.name  # 유저 아이디
        username_id: str = message.author.id
        global participant
        global option

        user_message.lower()

        print(f'{username} said: "{user_message}" ({channel})')

        if (user_message == 'join' or user_message == '-j') and Game.start == False:
            if Game.start == True:
                await message.channel.send("The game has already started")
            elif len(participant) == 4:
                await message.channel.send("participants are maxed out")
            elif any(username_id == p.id for p in participant):
                await message.channel.send(f'{nickname_mention} has already joined the game')
            else:
                # 기존 코드
                new_player = Player(nickname, username_id)
                participant.append(new_player)
                await message.channel.send(f'{nickname_mention} has join the game')
                

        elif (user_message == 'leave' or user_message == '-l') and Game.start == False:
            for p in participant:
                if p.nickname == nickname:
                    participant.remove(p)
                    Player.player_pool -= 1
                    await message.channel.send(f'{nickname_mention} has left the game')
                    break
                else:
                    await message.channel.send(f'{nickname_mention} is not currently in the game')

        elif user_message == 'player list' or user_message == '-pl':
            player_list = player_listing(participant)
            await message.channel.send(player_list)

        elif (user_message == 'start' or user_message == '-s') and Game.start == False:
            # 더미 소환 코드
            #new_player = Player('dummy1', '1')
            #participant.append(new_player)

            #new_player = Player('dummy2', '2')
            #participant.append(new_player)

            # new_player = Player('dummy3', '3')
            # participant.append(new_player)

            # new_player = Player('dummy4', '4')
            # participant.append(new_player)

            # if len(participant) != 4:
            # await message.channel.send("There should be 4 players to start the game")
            # else:
            Game.start = True

            # shuffle card
            for num in range(len(Deck.card)):
                random_num = random.randrange(0, Deck.card_num)
                card_temp.append(Card.card[random_num])
                Deck.card.pop(random_num)
                Deck.card_num -= 1

            Deck.card = card_temp
            print(Deck.card)

            Deck.dump_pile = (Deck.card[-1])
            Deck.card.pop(-1)

            # shuffle participant
            for num in range(len(participant)):
                random_player = random.randrange(0, len(participant))
                participant_temp.append(participant[random_player])
                participant.pop(random_player)

            participant = participant_temp

            # 유저 순서
            await message.channel.send("The round goes as " + " -> " + "**" + " ".join(participant[i].nickname for i in range(len(participant))) + "**")

            # draw card
            for num in range(len(participant)):
                participant[num].first_hand = Deck.card[0]
                (Deck.card).pop(0)
                print(Deck.card)

            await message.channel.send("**" + participant[New_Game.turns].nickname + "**" + " turns")

            participant[New_Game.turns].second_hand = Deck.card[0]
            (Deck.card).pop(0)

            print(Deck.dump_pile)

            option.append(participant[New_Game.turns].first_hand)
            option.append(participant[New_Game.turns].second_hand)
            option.append(
                Deck.card_word[int(participant[New_Game.turns].first_hand) - 1])
            option.append(
                Deck.card_word[int(participant[New_Game.turns].second_hand) - 1])

            for num in range(len(participant)):
                if participant[num].second_hand == "0":
                    #user = await client.fetch_user(participant[num].id)
                    #await user.send("Your card is \"" + str(change_word(participant[num].first_hand)) + "\"")
                    # await message.author.send("Your card is \""+ str(change_word(participant[num].first_hand)) + "\"")
                    print("Your card is \"" +
                          str(change_word(participant[num].first_hand)) + "\"")
                else:
                    # user = await client.fetch_user(participant[num].id)
                    # await user.send("Your card is \""+ str(change_word(participant[num].first_hand)) + "\"", hidden = True)
                    # await message.author.send("Your card is \""+ str(change_word(participant[num].first_hand)) + "\"")
                    print("Your card are \"" + str(change_word(participant[num].first_hand)) + "\",\"" + str(
                        change_word(participant[num].second_hand)) + "\"")
                    
    client.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()