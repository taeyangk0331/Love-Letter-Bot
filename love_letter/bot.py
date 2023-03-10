import discord
import random
import time
from typing import List

participant = []

class Card:
    card : List[int] = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
    card_word : List[str] = ['guard', 'priest', 'baron', 'handmaid', 'prince', 'king', 'countess', 'princess']
    card_num : int = 16

    def __init__(self):
        self.dump_pile : List[str] = []


class Player:
    start : bool = False
    turns : int = 0

    def __init__(self, nickname, id):
        self.nickname = nickname
        self.guard_ability = 0
        self.id = id
        self.first_hand = ""
        self.second_hand = ""


#player list method
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
    TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.Goc-9w.JUFIj3fmeFWE1vnUdC1RKrQiG3HtjhBoJr971c' #토큰
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    participant_temp = []
    card_temp = []

    @client.event
    async def on_message(message):
        if message.author == client.user: #디스코드 봇이 본인 메세지에 반응 방지
            return

        username : str = message.author #유저 이름
        user_message : str = message.content #유저 메세지
        channel : str = message.channel #체널 이름
        nickname_mention : str = message.author.name #유저 아이디(highlight)
        nickname : str = message.author.name #유저 아이디
        username_id : str = message.author.id
        global participant

        print(f'{username} said: "{user_message}" ({channel})')

        if (user_message == 'join' or user_message == '-j') and Player.start == False:
            if Player.start == True:
                await message.channel.send("The game has already started")
            elif len(participant) == 4:
                await message.channel.send("participants are maxed out")
            elif any(username_id == p.id for p in participant):
                await message.channel.send(f'{nickname_mention} has already joined the game')
            else:
                #기존 코드
                #new_player = Player(nickname, username_id)
                #participant.append(new_player)
                #await message.channel.send(f'{nickname_mention} has join the game')
                pass

        elif (user_message == 'leave' or user_message == '-l') and Player.start == False:
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

        elif (user_message == 'start' or user_message == '-s') and Player.start == False:
            #더미 소환 코드
            new_player = Player('dummy1', '1')
            participant.append(new_player)

            new_player = Player('dummy2', '2')
            participant.append(new_player)

            new_player = Player('dummy3', '3')
            participant.append(new_player)

            new_player = Player('dummy4', '4')
            participant.append(new_player)

            if len(participant) != 4:
                await message.channel.send("There should be 4 players to start the game")
            else:
                Player.start = True

                Deck = Card()
                
                #shuffle card
                for num in range(len(Deck.card)):
                    random_num = random.randrange(0, Deck.card_num)
                    card_temp.append(Deck.card[random_num])
                    Deck.card.pop(random_num)
                    Deck.card_num -= 1

                Deck.card = card_temp

                dump_card = Deck.card[-1]
                Deck.card.pop(-1)

                #shuffle participant
                for num in range(len(participant)):
                    random_player = random.randrange(0, len(participant))
                    participant_temp.append(participant[random_player])
                    participant.pop(random_player)
                
                participant = participant_temp

                await message.channel.send("The round goes as " + " -> " + "**" + " ".join(participant[i].nickname for i in range(len(participant))) + "**") #유저 순서

                #draw card
                for num in range(len(participant)):
                    participant[num].first_hand = Deck.card[0]
                    #user = await client.fetch_user(participant[num].id)
                    #await user.send("Your card is \""+ str(change_word(participant[num].first_hand)) + "\"")
                    await message.author.send("Your card is \""+ str(change_word(participant[num].first_hand)) + "\"")
                    Deck.card.pop(0)

                await message.channel.send("**" + participant[Player.turns].nickname + "**" + " turns")

        elif (participant[Player.turns].id == username_id) or (message.content.startswith(participant[Player.turns].first_hand)):
            pass

                
                    
                
    client.run(TOKEN)