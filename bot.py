import discord
import random
import asyncio
import time

player_dict = {'dummy1' : [], 'dummy2': [], 'dummy3': [], 'dummy4': []}
player_dict_shuffled = {}
turns = 0
player_pool = 3
ability = 0
card_word = ['guard', 'priest', 'baron', 'handmaid', 'prince', 'king', 'countess', 'princess']

async def send_message(message, user_message, is_private): #개인으로 메세지 보는 코드
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)

    except Exception as e:
        print(e)

def player_listing(player_dict):
    sentence = ''
    for player in player_dict:
        sentence += player
        sentence += ' '
    sentence += ' joined the game'
    print(sentence)
    return sentence

async def draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool):
    if turns != player_pool:
        turns += 1
        for find_zero in range(2):
            #print(list(player_dict_shuffled.values())[0][0])
            if (list(player_dict_shuffled.values())[turns][find_zero]) == 0:
                list(player_dict_shuffled.values())[turns][find_zero] = int(shuffled_card[0])
                shuffled_card.pop(0)
            
        await message.channel.send("**" + list(player_dict_shuffled)[turns] + "**" + " turns")
        list(player_dict_shuffled.keys())[turns]

        print(player_dict_shuffled)
        

        return turns
    else:
        turns = 0
        return turns



def run_discord_bot():
    TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.GVh5Kk.9ljnHIhTGK4zIS9Pt5vXNhwc6zUZBUzae3epMc' #토큰
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    shuffled_card = []


    @client.event #시작 부팅
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        global turns
        global player_pool
        global ability
        global dump_pile
        global card_num
        if message.author == client.user: #디스코드 봇이 본인 메세지에 반응 방지
            return

        
        username = str(message.author) #유저 이름
        user_message = str(message.content) #유저 메세지
        channel = str(message.channel) #채널 이름 (일반)
        nickname_mention = str(message.author.mention) #유저 아이디(mention)
        nickname = str(message.author.name) #유저 아이디


        print(f'{username} said: "{user_message}" ({channel})')

        if channel == 'loveletter':
            if user_message == 'join':
                if nickname in player_dict:
                    await message.channel.send(f'{nickname_mention} has already joined the game')
                else:
                    await message.channel.send(f'{nickname_mention} has join the game')
                    player_dict[nickname] = [0, 0]
                    #await message.channel.send(player_dict)

            elif user_message == 'leave':
                if nickname in player_dict:
                    await message.channel.send(f'{nickname_mention} has left the game')
                    del player_dict[nickname]
                    #await message.channel.send(player_dict)
                else:
                    await message.channel.send(f'{nickname_mention} is not in the game')

            elif user_message == 'joined players':
                player_list = player_listing(player_dict)
                await message.channel.send(player_list)

            elif user_message == 'start':
                if len(player_dict) == 4:
                    card_num = 16
                    card = [5, 5, 5, 6, 6, 6, 6, 5, 4, 4, 4, 4, 2, 2, 2, 2]
                    dump_pile = []

                    for shuffled in range(len(card)):
                        random_num = random.randrange(0, card_num)
                        shuffled_card.append(card[random_num])
                        card.pop(random_num)
                        card_num -= 1
                        #print(shuffled_card)
                        #print(card_num)
                        #print(card)

                    before = await message.channel.send("shuffling cards")
                    time.sleep(0.2)
                    for loop in range(2):
                        before = await before.edit(content = "shuffling cards.")
                        time.sleep(0.2)
                        before = await before.edit(content = "shuffling cards..")
                        time.sleep(0.2)
                        before = await before.edit(content = "shuffling cards...")
                        time.sleep(0.2)
                    await before.edit(content = "done!")

                    dump_card = shuffled_card[-1]
                    shuffled_card.pop(-1)
                    #print(dump_card)
                    #print(shuffled_card)

                    for shuffle in range(len(player_dict)):
                        #print(shuffle)
                        random_player = random.choice(list(player_dict))
                        player_dict.pop(random_player)
                        player_dict_shuffled[random_player] = [0, 0]

                    before = await message.channel.send("shuffling player order")
                    time.sleep(0.2)
                    for loop in range(2):
                        before = await before.edit(content = "shuffling player order.")
                        time.sleep(0.2)
                        before = await before.edit(content = "shuffling player order..")
                        time.sleep(0.2)
                        before = await before.edit(content = "shuffling player order...")
                        time.sleep(0.2)
                    await before.edit(content = "done!")

                    await message.channel.send("The round goes as " + " -> " + "**" + " ".join(player_dict_shuffled) + "**") #유저 순서
                    time.sleep(0.2)

                    for draw_card in player_dict_shuffled:
                        player_dict_shuffled[draw_card][0] = shuffled_card[0]
                        shuffled_card.pop(0)

                    await message.channel.send("**" + list(player_dict_shuffled)[turns] + "**" + " turns")
                    await message.channel.send("Please **\'check\'** the card!")

                    #print(shuffled_card)

                else:
                    await message.channel.send("There should be 4 players to start the game")

            elif (nickname == str(list(player_dict_shuffled.keys())[turns]) or (message.content.startswith('check'))):
                if turns != 4:
                    for find_zero in range(2):
                        #print(list(player_dict_shuffled.values())[0][0])
                        if (list(player_dict_shuffled.values())[turns][find_zero]) == 0:
                            list(player_dict_shuffled.values())[turns][find_zero] = int(shuffled_card[0])
                            shuffled_card.pop(0)
                        elif (list(player_dict_shuffled.values())[turns][find_zero]) == 10:
                            list(player_dict_shuffled.values())[turns][find_zero] = int(shuffled_card[0])
                            shuffled_card.pop(0)
                    list(player_dict_shuffled.keys())[turns]
                    await message.author.send(str(list(player_dict_shuffled.values())[turns][0]) + ' ' + str(list(player_dict_shuffled.values())[turns][1]))

                    list(player_dict_shuffled.values())[turns]

                    print(player_dict_shuffled)
                    print(dump_pile)

                else:
                    turns = 0
                
            elif (nickname == str(list(player_dict_shuffled.keys())[turns]) or (message.content.startswith(str(list(player_dict_shuffled.values())[turns][0])) or (user_message in str(card_word)))):
                action = str(list(player_dict_shuffled.values())[turns][0])

                async def guard_choose_player(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return m

                def guard_guess_player(m):
                    if player_dict_shuffled.keys() in m.content:
                        return 

                def priest(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return m

                def baron(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return m

                def prince(m):
                    if (m.content in list(player_dict_shuffled.keys()) or m.content == 'myself'):
                        return m

                def king(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return m

                def princess(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return m

                async def is_protected(player):
                    for num in range(2):
                        if player_dict_shuffled[player][num] == 10:
                            await message.channel.send(player + 'is protected\nget rekt bitch')
                        
                    return

                def result(m):
                    return m.content == 'result'

                if action == '1' or message.content.startswith('guard'): #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the guard")
                    await message.channel.send('Choose the player')
                    guard_choose_player_ = await client.wait_for('message', check = guard_choose_player)
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(guard_choose_player_.content) + ' please guess the card (1 ~ 8)')
                    guard_guess_player_ = await client.wait_for('message', check = guard_guess_player)
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '2' or message.content.startswith('priest'):#done yay
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the priest (2)")
                    await message.channel.send('Choose the player')
                    priest_ = await client.wait_for('message', check = priest)
                    before = await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + 
                        str(priest_.content))
                    for num in range(2):
                        if player_dict_shuffled[priest_.content][num] == 10:
                            await before.edit(content = (priest_.content + ' is protected\nget rekt bitch'))
                            break
                        elif player_dict_shuffled[priest_.content][num] != 0:
                            await before.edit(content = (str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + 
                        str(priest_.content) + '\n' + str(priest_.content) + '\'s card could be seen in private message'))
                            await message.author.send(player_dict_shuffled[priest_.content][num])
                            break
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '3' or message.content.startswith('baron'): #insert elimination
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the baron (3)")
                    await message.channel.send('Choose the player')
                    baron_ = await client.wait_for('message', check = baron)
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + 
                            str(baron_.content))
                    for find_zero in range(2):
                        if player_dict_shuffled[baron_.content][find_zero] != 0 and player_dict_shuffled[baron_.content][find_zero] != 10:
                            await message.channel.send('Comparing both players')
                            time.sleep(2)
                            await message.channel.send('Type **\'result\'** to see the result!')
                            result_ = await client.wait_for('message', check = result)
                            if player_dict_shuffled[baron_.content][find_zero] > list(player_dict_shuffled.values())[turns][1]: #opponent > me
                                await message.channel.send(baron_.content + ' has won the battle!\n' + str(list(player_dict_shuffled.keys())[turns]) + ' is eliminated')
                                break
                                #insert elimination
                            elif player_dict_shuffled[baron_.content][find_zero] < list(player_dict_shuffled.values())[turns][1]:
                                await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has won the battle!\n' + baron_.content + ' is eliminated')
                                break
                                #insert elimination
                            else:
                                await message.channel.send('Both players have tied')
                                break
                        else:
                            await message.channel.send(baron_.content + ' is protected\nget rekt bitch')
                            break
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 10
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)
                    print(list(player_dict_shuffled.values()))

                elif action == '4' or message.content.startswith('handmaid'): #done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the handmaid (4)")
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns] + " is protected until own turn"))
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 10
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '5' or message.content.startswith('prince'): #princess elimination
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the prince (5)")
                    await message.channel.send('Choose the player\nIf the player choose own card, type \'myself\'')
                    prince_ = await client.wait_for('message', check = prince)
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(prince_.content))
                    if prince_.content == 'myself':
                        await message.channel.send(str(list(player_dict_shuffled.values())[turns] + '\'s card was ' + str(list(player_dict_shuffled.values())[turns][1])))
                        dump_pile.append(list(player_dict_shuffled.values())[turns][1])
                        list(player_dict_shuffled.values())[turns][1] = int(shuffled_card[0])
                        shuffled_card.pop(0)
                    else:
                        for find_zero in range(2):
                            if player_dict_shuffled[prince_.content][find_zero] == 10:
                                await message.channel.send(prince_.content + ' is protected\nget rekt bitch')
                                await message.channel.send('Due to handmaid hidden passive ' + str(list(player_dict_shuffled.values())[turns] + ' has open other card'))
                                await message.channel.send(str(list(player_dict_shuffled.values())[turns] + '\'s card was ' + str(list(player_dict_shuffled.values())[turns][1])))
                                dump_pile.append(list(player_dict_shuffled.values())[turns][1])
                                list(player_dict_shuffled.values())[turns][1] = int(shuffled_card[0])
                                shuffled_card.pop(0)
                                break
                            elif player_dict_shuffled[prince_.content][find_zero] != 0:
                                if player_dict_shuffled[prince_.content][find_zero] != 8:
                                    await message.channel.send(prince_.content + '\'s card was ' + str(player_dict_shuffled[prince_.content][find_zero]))
                                    dump_pile.append(player_dict_shuffled[prince_.content][find_zero])
                                    player_dict_shuffled[prince_.content][find_zero] = int(shuffled_card[0])
                                    shuffled_card.pop(0)
                                    break
                                else:
                                    await message.channel.send(str(player_dict_shuffled[prince_.content][find_zero]) + '\n' + [prince_.content] + ' has been eliminated')
                                    break
                                    #eliminate
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '6' or message.content.startswith('king'): #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the king (6)")
                    await message.channel.send('Choose the player')
                    king_ = await client.wait_for('message', check = king)
                    chat = await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(king_.content) + ' to trade card')
                    time.sleep(0.1)
                    await chat.edit(content = 'The card is traded')
                    for find_zero in range(2):
                        if player_dict_shuffled[king_.content][find_zero] == 10:
                            await message.channel.send(king_.content + ' is protected\nget rekt bitch')
                            break
                        elif player_dict_shuffled[king_.content][find_zero] != 0:
                            temp = list(player_dict_shuffled.values())[turns][1]
                            list(player_dict_shuffled.values())[turns][1] = player_dict_shuffled[king_.content][find_zero]
                            player_dict_shuffled[king_.content][find_zero] = temp
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '7' or message.content.startswith('countess'): #not done
                    if (list(player_dict_shuffled.values())[turns][1]) == 5 or (list(player_dict_shuffled.values())[turns][1] == 6):
                        await message.author.send("You are not allow to choose countesss because your hand has either king (6) or prince (5)")

                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the countess (6)")
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '8' or message.content.startswith('princess'): #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the princess")
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " is elminiated")
                    del player_dict_shuffled[turns]
                    player_pool -= 1
                    princess_ = await client.wait_for('message', check = princess)
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)
                else:
                    print('default')
                    

            elif message.content.startswith('pooh'):
                num = 0
                def check(m):
                    return m.content == 'is he?' and m.channel == channel

                channel = message.channel
                await channel.send('pooh is gay bitch')

                if num == 0:
                        msg = await client.wait_for('message', check=check)
                        await channel.send(f'gay bitch pooh!')

            elif user_message == 'owo':
                await message.channel.send('owo')

            else:
                return

            

        #if user_message[0] == '?': #개인 메세지로 입력
            #user_message = user_message[1:]
            #await send_message(message, user_message, is_private=True)
        #else:
            #await send_message(message, user_message, is_private=False)

    client.run(TOKEN)
    