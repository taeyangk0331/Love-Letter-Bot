import discord
import random
import asyncio
import time

player_dict = {'dummy1': [], 'dummy2': [], 'dummy3': [], 'dummy4': []}
player_dict_shuffled = {}
turns = 0
player_pool = 3
guard_ability = 0
card_word = ['guard', 'priest', 'baron', 'handmaid', 'prince', 'king', 'countess', 'princess']
player_id = []

def player_listing(player_dict):
    sentence = ''
    for player in player_dict:
        sentence += player
        sentence += ' '
    sentence += ' joined the game'
    print(sentence)
    return sentence

def change_word(num):
    if num == '1':
        return 'Guard (1)'
    elif num == '2':
        return 'Priest (2)'
    elif num == '3':
        return 'Baron (3)'
    elif num == '4':
        return 'Handmaid (4)'
    elif num == '5':
        return 'Prince (5)'
    elif num == '6':
        return 'King (6)'
    elif num == '7':
        return 'Countess (7)'
    elif num == '8':
        return 'Princess (8)'

async def draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool):
    if turns != player_pool:
        turns += 1
        for find_zero in range(2):
            #print(list(player_dict_shuffled.values())[0][0])
            if (list(player_dict_shuffled.values())[turns][find_zero]) == 0:
                list(player_dict_shuffled.values())[turns][find_zero] = int(shuffled_card[0])
                shuffled_card.pop(0)
            
        await message.channel.send("**" + list(player_dict_shuffled)[turns] + "**" + " turns")
        await message.channel.send("Dump pile = " + str(dump_pile))
        await message.channel.send("Please **\'check\'** the card!")
        list(player_dict_shuffled.keys())[turns]

        print(player_dict_shuffled)
        print(turns)
        print(player_pool)

        

        return turns
    else:
        turns = 0
        return turns



def run_discord_bot():
    TOKEN = 'MTA2MDA2NzE5NDExNDk1MzI0Nw.Goc-9w.JUFIj3fmeFWE1vnUdC1RKrQiG3HtjhBoJr971c' #토큰
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
        global guard_ability
        global dump_pile
        global card_num
        if message.author == client.user: #디스코드 봇이 본인 메세지에 반응 방지
            return

        
        username = str(message.author) #유저 이름
        user_message = str(message.content) #유저 메세지
        channel = str(message.channel) #채널 이름 (일반)
        nickname_mention = str(message.author.mention) #유저 아이디(mention)
        nickname = str(message.author.name) #유저 아이디
        username_id = str(message.author.id)



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
                    player_id.remove(message.author.id)
                    #await message.channel.send(player_dict)
                else:
                    await message.channel.send(f'{nickname_mention} is not in the game')

            elif user_message == 'joined players':
                player_list = player_listing(player_dict)
                await message.channel.send(player_list)

            elif user_message == 'start':
                if len(player_dict) == 4:
                    card_num = 16
                    card = [1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 5, 5, 6, 7, 8]
                    dump_pile = []

                    for shuffled in range(len(card)):
                        random_num = random.randrange(0, card_num)
                        shuffled_card.append(card[random_num])
                        card.pop(random_num)
                        card_num -= 1
                        #print(shuffled_card)
                        #print(card_num)
                        #print(card)

                    #before = await message.channel.send("shuffling cards")
                    #time.sleep(0.2)
                    #for loop in range(2):
                        #before = await before.edit(content = "shuffling cards.")
                        #time.sleep(0.2)
                        #before = await before.edit(content = "shuffling cards..")
                        #time.sleep(0.2)
                        #before = await before.edit(content = "shuffling cards...")
                        #time.sleep(0.2)
                    #await before.edit(content = "done!")

                    dump_card = shuffled_card[-1]
                    shuffled_card.pop(-1)
                    #print(dump_card)
                    #print(shuffled_card)

                    for shuffle in range(len(player_dict)):
                        #print(shuffle)
                        random_player = random.choice(list(player_dict))
                        player_dict.pop(random_player)
                        player_dict_shuffled[random_player] = [0, 0]

                    #before = await message.channel.send("shuffling player order")
                    #time.sleep(0.2)
                    #for loop in range(2):
                        #before = await before.edit(content = "shuffling player order.")
                        #time.sleep(0.2)
                        #before = await before.edit(content = "shuffling player order..")
                        #time.sleep(0.2)
                        #before = await before.edit(content = "shuffling player order...")
                        #time.sleep(0.2)
                    #await before.edit(content = "done!")

                    await message.channel.send("The round goes as " + " -> " + "**" + " ".join(player_dict_shuffled) + "**") #유저 순서
                    time.sleep(0.2)

                    for draw_card in player_dict_shuffled:
                        player_dict_shuffled[draw_card][0] = shuffled_card[0]
                        shuffled_card.pop(0)

                    for player in player_id:
                        user = await client.fetch_user(player)
                        await user.send("hello")
                    #author = message.author
                    #author_name = 'BeCreative'
                    #private_channel = await author.create_dm()
                    #await private_channel.send(f"Hello {author_name}, this is a private message from the bot.")

                    

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

                    await message.author.send('You have [ **' + change_word(str(list(player_dict_shuffled.values())[turns][0])) + '** | **' + change_word(str(list(player_dict_shuffled.values())[turns][1])) + '** ] in your hand')

                    list(player_dict_shuffled.values())[turns]

                    print(player_dict_shuffled)
                    print(dump_pile)

                else:
                    turns = 0
                
            elif (nickname == str(list(player_dict_shuffled.keys())[turns]) or (message.content.startswith(str(list(player_dict_shuffled.values())[turns][0])) or (user_message in str(card_word))) and guard_ability  == 0):
                action = str(list(player_dict_shuffled.values())[turns][0])

                def guard_choose_player(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return True

                def guard_guess_player(m):
                    if (m.content in card_word):
                        return True
                    elif int(m.content) < 10 or int(m.content) > 0:
                        return True

                def priest(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return True

                def baron(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return True

                def prince(m):
                    if (m.content in list(player_dict_shuffled.keys()) or m.content == 'myself'):
                        return True

                def king(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return True

                def princess(m):
                    if m.content in list(player_dict_shuffled.keys()):
                        return True

                def result(m):
                    return m.content == 'result'

                if action == '1' or message.content.startswith('guard'): #not done
                    guard_ability = 1
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the guard (1)")
                    await message.channel.send('Choose the player')
                    guard_choose_player_ = await client.wait_for('message', check = guard_choose_player) #choosing player
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(guard_choose_player_.content) + ' please guess the card (1 ~ 8)')
                    guard_guess_player_ = await client.wait_for('message', check = guard_guess_player)#choosing card
                    print(int(guard_guess_player_.content) in player_dict_shuffled[guard_choose_player_.content])
                    print(player_dict_shuffled[guard_choose_player_.content])
                    print(guard_guess_player_.content)
                    print(type(guard_guess_player_.content))
                    #이거 고쳐야함
                    #고쳐야할점 user_message가 1일때 loop해서 계속 You are not allow to guess guard 나오게 하기
                    #local variable match referenced before assignement
                    #elimination 시발거
                    #나중에 id 로 user.fetch해서 유저에게 개인으로 DM 보내기
                    #카드 끝나고 비교
                    #win point
                    if guard_guess_player_.content == '1':
                        while True:
                            await message.channel.send("You are not allow to guess guard (1)\nChoose another number")
                            guard_guess_player_ = await client.wait_for('message', check = guard_guess_player)#choosing card
                            print('come out')
                            if guard_guess_player_.content != '1':
                                print("guard guess player content is not 1")
                                break
                    if int(guard_guess_player_.content) in player_dict_shuffled[guard_choose_player_.content]:
                        print("debug True")
                        del player_dict_shuffled[guard_choose_player_.content]
                        await message.channel.send(str(guard_choose_player_.content) + " has been eliminated")
                        player_pool -= 1
                        guard_ability = 0
                        dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                        list(player_dict_shuffled.values())[turns][0] = 0
                        turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)
                    elif int(guard_guess_player_.content) not in player_dict_shuffled[guard_choose_player_.content]:
                        print("debug False")
                        await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has guessed wrong card")
                        guard_ability = 0
                        dump_pile.append(list(player_dict_shuffled.values())[turns][0])
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
                            before = await message.channel.send('Comparing both players')
                            time.sleep(0.2)
                            for loop in range(2):
                                before = await before.edit(content = "Comparing both players.")
                                time.sleep(0.2)
                                before = await before.edit(content = "Comparing both players..")
                                time.sleep(0.2)
                                before = await before.edit(content = "Comparing both players...")
                                time.sleep(0.2)
                            await message.channel.send('Type **\'result\'** to see the result!')
                            result_ = await client.wait_for('message', check = result)
                            if player_dict_shuffled[baron_.content][find_zero] > list(player_dict_shuffled.values())[turns][1]: #opponent > me
                                await message.channel.send(baron_.content + ' has won the battle!\n' + str(list(player_dict_shuffled.keys())[turns]) + ' is eliminated')
                                del player_dict_shuffled[list(player_dict_shuffled.keys())[turns]]
                                player_pool -= 1
                                break
                            elif player_dict_shuffled[baron_.content][find_zero] < list(player_dict_shuffled.values())[turns][1]:
                                await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has won the battle!\n' + baron_.content + ' is eliminated')
                                del player_dict_shuffled[baron_.content]
                                player_pool -= 1
                                break
                            else:
                                await message.channel.send('Both players have tied')
                                break
                        else:
                            await message.channel.send(baron_.content + ' is protected\nget rekt bitch')
                            break
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)
                    print(list(player_dict_shuffled.values()))

                elif action == '4' or message.content.startswith('handmaid'): #done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the handmaid (4)")
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns] + " is protected until own turn"))
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 10
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif (action == '5' or message.content.startswith('prince')) and (list(player_dict_shuffled.values())[turns][1]) != 7: #princess elimination
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the prince (5)")
                    await message.channel.send('Choose the player\nIf the player choose own card, type \'myself\'')
                    prince_ = await client.wait_for('message', check = prince)
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(prince_.content))
                    if prince_.content == 'myself':
                        await message.channel.send(str(list(player_dict_shuffled.keys())[turns] + '\'s card was ' + str(list(player_dict_shuffled.values())[turns][1])))
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

                elif (action == '5' or message.content.startswith('prince')) and (list(player_dict_shuffled.values())[turns][1]) == 7:
                    await message.channel.purge(limit=1)
                    await message.channel.send(content = "You are not allow to use either prince(5) or king(6) if you have countess(7) in your hand")

                elif action == '6' or message.content.startswith('king') and (list(player_dict_shuffled.values())[turns][1]) != 7: #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the king (6)")
                    await message.channel.send('Choose the player')
                    king_ = await client.wait_for('message', check = king)
                    chat = await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + ' has chosen ' + str(king_.content) + ' to trade card')
                    time.sleep(0.2)
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

                elif action == '6' or message.content.startswith('king') and (list(player_dict_shuffled.values())[turns][1]) == 7:
                    await message.channel.purge(limit=1)
                    await message.channel.send(content = "You are not allow to use either prince(5) or king(6) if you have countess(7) in your hand")

                elif ((action == '7' or message.content.startswith('countess'))): #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the countess (7)")
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
                    list(player_dict_shuffled.values())[turns][0] = 0
                    turns = await draw_card_func(player_dict_shuffled, shuffled_card, message, turns, player_pool)

                elif action == '8' or message.content.startswith('princess'): #not done
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " has choose the princess")
                    await message.channel.send(str(list(player_dict_shuffled.keys())[turns]) + " is elminiated")
                    del player_dict_shuffled[str(list(player_dict_shuffled.keys())[turns])]
                    player_pool -= 1
                    dump_pile.append(list(player_dict_shuffled.values())[turns][0])
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
    