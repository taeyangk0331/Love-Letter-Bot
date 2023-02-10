import random
import discord
from discord.ext import commands
import asyncio

TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.GVh5Kk.9ljnHIhTGK4zIS9Pt5vXNhwc6zUZBUzae3epMc' #토큰
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def guard(user_message):
    pass

async def draw_card_func(player_dict_shuffled, shuffled_card, message, count):

    if count != 4:
        for find_zero in range(2):
            #print(list(player_dict_shuffled.values())[0][0])
            if (list(player_dict_shuffled.values())[count][find_zero]) == 0:
                list(player_dict_shuffled.values())[count][find_zero] = int(shuffled_card[0])
                shuffled_card.pop(0)
        await message.channel.send("**" + list(player_dict_shuffled)[count] + "**" + " turns")
        list(player_dict_shuffled.keys())[count]
        await message.author.send(list(player_dict_shuffled.values())[count])

        count += 1
        return count
    else:
        count = 0
        return count



@client.event
async def init(player_dict, message, user_message):

    count = 0
    card_num = 16
    card = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
    dump__pile = []

    shuffled_card = []
    for shuffle in range(len(card)): #카드 섞기
        random_num = random.randrange(0,card_num)
        shuffled_card.append(card[random_num])
        card.pop(random_num)
        card_num -= 1
        #print(shuffled_card)
        #print(card_num)
        #print(card)

    
    dump_card = shuffled_card[-1]
    shuffled_card.pop(-1)
    #print(dump_card)
    #print(shuffled_card)

    player_dict_shuffled = {}

    for shuffle in range(len(player_dict)): #유저 섞기
        #print(shuffle)
        random_player = random.choice(list(player_dict))
        player_dict.pop(random_player)
        player_dict_shuffled[random_player] = [0, 0]
    
    await message.channel.send("The round goes as " + " -> "+ "**" + " ".join(player_dict_shuffled) + "**") #유저 순서

    for draw_card in player_dict_shuffled:
        player_dict_shuffled[draw_card][0] = shuffled_card[0]
        shuffled_card.pop(0)

    #print(player_dict_shuffled)

    #print(shuffled_card)

    count = await draw_card_func(player_dict_shuffled, shuffled_card, message, count)

    #print(user_message)

    print(user_message in list(player_dict_shuffled.values()))

    if(user_message in list(player_dict_shuffled.values())):
        print("debug")
        match user_message:
            case 1:
                await guard(user_message)
                count = await draw_card_func(player_dict_shuffled, shuffled_card, message, count)
            case 2:
                pass


    #key = list(player_dict)[0]

    #print('first key is ' + str(key))
    

    #print(shuffled_card)
    #print(player_dict)


