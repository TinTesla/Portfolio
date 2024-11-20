
# Stage 1: Dependencies <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
import random
import copy

# Stage 2: Functions <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
# Just a blank print to seperate lines. 
def line_break():
    print('')

#_____________________________________________________
# Empty structure of decks
def new_deck():
    return {"suits": [],
            "values": [],
            "ids": []}
#_____________________________________________________
# Building Shoe in New Deck Order
def new_multi_deck():
    # Initial Deck build
    # Unicode icons
    spade = '\u2660'
    club = '\u2663'
    heart = '\u2665'
    diamond = '\u2666'

    # Setting up unique features
    suits = [spade, diamond, club, heart]
    faces = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    # Initial setup
    raw_deck = {"suits": [], "values": [], "ids": []}
    
    # Loop to initialize all unique combinations in both bins
    for suit_index, suit in enumerate(suits):
        if suit_index < 2:
            for face_index, face in enumerate(faces):
                raw_deck["suits"].append(suit + face)
                raw_deck["values"].append(values[face_index])
        else:
            for face_index, face in enumerate(reversed(faces)):
                raw_deck["suits"].append(suit + face)
                raw_deck["values"].append(values[-face_index-1])

    # Now building a multi-deck deck in New Deck Order
    output_deck = new_deck()

    # Loop to make a multi-deck deck
    for deck in range(8):  # << You can alter the 8 of range(8) if you want more/less decks in the shoe
        output_deck["suits"] += raw_deck["suits"]
        output_deck["values"] += raw_deck["values"]

    # Separate loop to create unique IDs for each of the cards in the multi-deck deck
    for id in range(len(output_deck["suits"])):
        output_deck["ids"].append(id)
    
    #Return the Shoe in New Deck Order
    return output_deck

#_____________________________________________________
# Takes an input, and randomly selects an index from the original, to one by one assemble a shuffled deck
def randomized_shuffling(input_deck):
    # Directly modify the input deck
    output_deck = copy.deepcopy(input_deck)
    
    # Shuffle the deck using Python's built-in shuffle
    combined_list = list(zip(output_deck["suits"], output_deck["values"], output_deck["ids"]))
    random.shuffle(combined_list)
    
    # Unzip the shuffled deck
    output_deck["suits"], output_deck["values"], output_deck["ids"] = zip(*combined_list)
    
    #Return the shuffled shoe
    return output_deck

#_____________________________________________________
# Takes an input, and shuffles is in an alternating pattern
def interlaced_shuffling(input_deck):
    # Perform a random number of interlaced shuffles
    shuffle_count = random.randint(10, 20)
    
    for _ in range(shuffle_count):
        # Bin shift to prepare for the next shuffle
        output_deck = new_deck()

        # Interlace shuffle
        half = len(input_deck["suits"]) // 2
        for card in range(half):
            for key in ["suits", "values", "ids"]:
                output_deck[key].append(input_deck[key][half + card])
                output_deck[key].append(input_deck[key][card])
        
        # Prepare for the next shuffle iteration
        input_deck = output_deck  
    
    return output_deck
#_____________________________________________________
# Takes 2 inputs, and seperates them accross 52 bins in a random order before reassembling by bin
def rotary_shuffling(shoe_deck, discard_deck):    
    # Merge shoe_deck and discard_deck into temp_deck
    temp_deck = new_deck()
    for key in temp_deck:
        temp_deck[key].extend(discard_deck[key])
        temp_deck[key].extend(shoe_deck[key])
        
    # Reset shoe_deck and discard_deck
    shoe_deck = new_deck()
    discard_deck = new_deck()
    
    # Setup rotary shuffler with 52 bins
    rotary_shuffler = {f"Bin {id}": new_deck() for id in range(52)}
    open_bins = list(range(52))
    
    # Distribute all cards into bins
    while temp_deck["suits"]:
        # Exit failsafe
        if not open_bins:
            break
        
        current_slot = random.choice(open_bins)
        slot_name = f"Bin {current_slot}"
        
        # Transfer cards to the bin
        if len(rotary_shuffler[slot_name]["suits"]) < 8:
            for key in ["suits", "values", "ids"]:
                rotary_shuffler[slot_name][key].append(temp_deck[key].pop(0))
            if len(rotary_shuffler[slot_name]["suits"]) == 8:
                open_bins.remove(current_slot)
                
    # Reassemble shoe_deck from bins
    slot_bins = list(range(52))
    opposite_slot = random.choice(slot_bins) + 25
    
    while slot_bins:
        opposite_slot %= 52
        slot_name = f"Bin {opposite_slot}"
        
        for key in ["suits", "values", "ids"]:
            shoe_deck[key].extend(rotary_shuffler[slot_name][key])
        
        slot_bins.remove(opposite_slot)
        opposite_slot += 1
        
    #Return the decks
    return shoe_deck, discard_deck

#_____________________________________________________
# Variable loop to check for valid inputs from the user
def input_loop(x_options):
    # dynamic dictionary access
    keys = list(x_options.keys())
    
    #_____________________________________________________   
    # dictionary seperation
    input_selection = x_options[keys[0]]
    valid_options = x_options[keys[1]]
    prompt_text = x_options[keys[2]]
    help_texts = x_options[keys[3]]
    default_value = x_options[keys[4]]
    #_____________________________________________________   
    # tracker bins
    attempts = 0
    max_attempts = 5
    
    while attempts < max_attempts:
        user_input = input(prompt_text).strip()
        #_____________________________________________________   
        # Check for help request
        if user_input.upper() == 'HELP':
            for text in help_texts:
                print(text)
            continue # reset to skip further checks
        #_____________________________________________________          
        # integer based inputs (used for hold/round)
        elif user_input.isdigit():
            user_input = int(user_input)
            # valid input exit
            if user_input in valid_options: #(for hold_options)
                input_selection = user_input
                print(f'Thank you, the value {user_input} has been selected.')
                break
            elif valid_options[0] == True: #(for round_options)
                input_selection = user_input
                print(f'Thank you, {user_input} rounds will be simulated.')
                break
            else:
                print('Sorry, that was an invalid response. Please try again.')
        #_____________________________________________________   
        # text based inputs (used for turn(1-3)/play/mode/skill/result)
        else:
            user_input = user_input.upper()
            # valid input exit
            if user_input in valid_options:
                input_selection = user_input
                print(f'Thank you, mode {user_input} has been selected.')
                break 
            else:
                print('Sorry, that was an invalid response. Please try again.')
        
        # bin update
        attempts += 1
    #_____________________________________________________   
    # max attempts exit
    if attempts >= max_attempts:
        print(f'Too many attempts have been made. The default option of {default_value} will be selected.')
        input_selection = default_value
    #_____________________________________________________ 
    # update + export
    x_options[keys[0]] = input_selection
    return x_options

# Result codes
def round_results(player_hand, dealer_hand, win_rates):
    # sums
    player_sum = sum(player_hand['values'])
    dealer_sum = sum(dealer_hand['values'])   
    #_____________________________________________________
    # Player blackjack
    if player_sum == 21 and len(player_hand['values']) == 2:
        if dealer_sum == 21 and len(dealer_hand['values']) == 2:
            win_rates["PJDJ"] += 1  # Push, each with blackjack
        elif dealer_sum == 21:
            win_rates["PpDp"] += 1  # ~Standard Push
        elif dealer_sum > 21:
            win_rates["PJDB"] += 1  # Player blackjack, dealer bust
        elif dealer_sum < 21:
            win_rates["PJDL"] += 1  # Player blackjack, dealer lost
        else:
            win_rates["Errors"] += 1  # Error bin
    #_____________________________________________________
    # Dealer blackjack        
    elif dealer_sum == 21 and len(dealer_hand['values']) == 2:
        if player_sum != 21:
            win_rates["PLDJ"] += 1  # Player lost, dealer blackjack
        else:
            win_rates["Errors"] += 1  # Error bin
    #_____________________________________________________
    # Player valid        
    elif player_sum <= 21:
        if dealer_sum <= 21:
            if player_sum > dealer_sum:
                win_rates["PWDL"] += 1  # Player wins, dealer lost
            elif player_sum < dealer_sum:
                win_rates["PLDW"] += 1  # Player loss, dealer wins
            elif player_sum == dealer_sum:
                win_rates["PpDp"] += 1  # Standard Push
            else:
                win_rates["Errors"] += 1  # Error bin
        else:
            win_rates["PWDB"] += 1  # Player wins, dealer bust
    #_____________________________________________________        
    # Player busts
    else:
        if dealer_sum <= 21:  # Dealer valid
            win_rates["PBDW"] += 1  # Player bust, dealer wins
        elif dealer_sum > 21:
            win_rates["PBDB"] += 1  # Player bust, dealer bust
        else:
            win_rates["Errors"] += 1  # Error bin

def ace_reset(hand):
    if 1 in hand['values']:
        hand_ace = hand['values'].index(1)
        hand['values'][hand_ace] = 11

def discard_transfer(hand, discard_deck):
    for key, value in hand.items():
            discard_deck[key] += value

# Card Dealing
def deal_card(import_deck, hand):
    for key in ["suits", "values", "ids"]:
        hand[key].append(import_deck[key].pop(0))

#Dealer's Turn
def dealer_play(import_deck, dealer_hand):
    #
    if sum(dealer_hand['values']) == 22:
        dealer_ace = 0 
        dealer_hand['values'][dealer_ace] = 1
    if sum(dealer_hand['values']) < 17:
        while sum(dealer_hand['values']) < 17:
            deal_card(import_deck, dealer_hand)
            if sum(dealer_hand['values']) > 21:
                if 11 in dealer_hand['values']:
                    dealer_ace = dealer_hand['values'].index(11)
                    dealer_hand['values'][dealer_ace] = 1

# Manual Play mode
def deal_loop_manual():
    # pulling global variables
    global skill_options,shoe_deck
    #_____________________________________________________   
    # initial setup
    draw_count = 0
    dealer_hand = new_deck()
    hand_1 = new_deck()
    player_hands = [hand_1]
    hand = 0
    skill_mode = skill_options['skill_input']

    #_____________________________________________________
    # initial draws
    for _ in range(2):
        deal_card(shoe_deck, player_hands[0])
        deal_card(shoe_deck, dealer_hand)
    #_____________________________________________________     
    # Hand iteration (if split)
    while hand < len(player_hands):
        # new hand reset
        draw_live = True
        ace_flip = False
        
        # Double Ace check
        if sum(player_hands[hand]['values']) == 22:
            player_hands[hand]['values'][0] = 1
            print("You were dealt 2 aces. One will be flipped to a value of 1.")
            ace_flip = True

        # instant BJ check
        if sum(player_hands[hand]['values']) == 21:
            print('Lucky you! You were dealt a Blackjack!')
            draw_live = False
            
        # Main branch
        while draw_live == True:
            #_____________________________________________________
            # Ace save check
            if sum(player_hands[hand]['values']) > 21:
                if 11 in player_hands[hand]['values']:
                    player_ace = player_hands[hand]['values'].index(11)
                    player_hands[hand]['values'][player_ace] = 1
                    print("You drew an Ace, but you almost went over. Ace flipped to 1")
                    print(f"Your hand is now {sum(player_hands[hand]['values'])}")
            #_____________________________________________________
            # print setting
            if skill_mode == "P":
                player_hand_text = player_hands[hand]['suits']
                dealer_single_text = dealer_hand['suits'][0]
            else:
                player_hand_text = sum(player_hands[hand]['values'])
                dealer_single_text = dealer_hand['values'][0]
            #_____________________________________________________
            # dictionary selection
            if draw_count == 0:
                if player_hands[hand]['values'][0] == player_hands[hand]['values'][1]:
                    hand_options = turn_options_1 #(S)tand, (H)it, spli(T), (D)ouble, (F)old
                elif ace_flip:
                    hand_options = turn_options_1 #(S)tand, (H)it, spli(T), (D)ouble, (F)old
                else:
                    hand_options = turn_options_2 #(S)tand, (H)it, (D)ouble, (F)old
            else:
                hand_options = turn_options_3 #(S)tand, (H)it

            #_____________________________________________________
            # Standard game loop            
            if sum(player_hands[hand]['values']) < 21:
                
                # Instant loss check
                if sum(dealer_hand['values']) != 21:
                    #_____________________________________________________                   
                    # pre-input message
                    if draw_count > 0:
                        if len(player_hands) > 1:
                            print(f"Hand {hand} is now {player_hand_text}.")
                        else:
                            print(f"Your hand is now {player_hand_text}.")
                            
                    else:
                        print(f"Dealer is showing {dealer_single_text}")
                        print(f"Your hand is {player_hand_text}. What would you like to do?")
                    #_____________________________________________________   
                    # initiate input prompt
                    hand_selection = input_loop(hand_options)
                    
                    #_____________________________________________________   
                    # input seperation
                    input_selection = hand_selection[list(hand_selection.keys())[0]]

                    if input_selection == 'H':
                        draw_count += 1
                        deal_card(shoe_deck, player_hands[hand])

                    elif input_selection == 'T':
                        draw_count += 1
                        # create new blank hand
                        player_hands.append([])
                        player_hands[hand+1] = new_deck()
                        # steal first card and place into new hand
                        for key in ["suits", "values", "ids"]:
                            player_hands[hand+1][key].append(player_hands[hand][key].pop(0))
                        # new secondary cards
                        deal_card(shoe_deck, player_hands[hand])
                        deal_card(shoe_deck, player_hands[hand+1])

                    elif input_selection == 'D':
                        draw_count += 1
                        draw_live = False
                        deal_card(shoe_deck, player_hands[hand])
                        # print update
                        if skill_mode == "P":
                            player_hand_text = player_hands[hand]['suits']
                        else:
                            player_hand_text = sum(player_hands[hand]['values'])
                        print(f"You drew one last card, making your hand {player_hand_text}.")

                    elif input_selection == 'F':
                        draw_live = False
                        print('You folded your hand.')

                    else: #Stand/ Default
                        draw_live = False
                        print(f"You stood with a hand of {player_hand_text}.")
                #_____________________________________________________                   
                # Dealer Blackjack
                else:
                    draw_live = False
            #_____________________________________________________
            # Bust / Blackjack / @21
            else:
                draw_live = False
        
        # next hand
        hand += 1
                
    #_____________________________________________________
    # Dealer's draw logic
    dealer_play(shoe_deck, dealer_hand)
                
    # final dealer hand print
    if skill_mode == "P":
        dealer_hand_text = dealer_hand['suits']
    else:
        dealer_hand_text = sum(dealer_hand['values'])
         
    if len(dealer_hand['suits']) == 2:
        print(f"Dealer stood with {dealer_hand_text}")
    else:
        print(f"Dealer drew to {dealer_hand_text}")
                    
    return player_hands, dealer_hand

# Auto Play mode
def deal_loop_auto():
    # pulling global variables
    global shoe_deck
    #_____________________________________________________   
    # initial setup
    draw_count = 0
    dealer_hand = new_deck()
    player_hand = new_deck()
    hold_threshold = hold_options['hold_input']
    skill_mode = skill_options['skill_input']
    #_____________________________________________________
    # initial draws
    for _ in range(2):
        deal_card(shoe_deck, player_hand)
        deal_card(shoe_deck, dealer_hand)
    #_____________________________________________________
    # Double Ace check
    if sum(player_hand['values']) == 22:
        player_hand['values'][0] = 1

    # instant BJ check
    if sum(player_hand['values']) == 21:
        draw_live = False
    else: 
        draw_live = True
    #_____________________________________________________
    # main loop
    while draw_live == True:
        #_____________________________________________________
        # ace flip check
        if sum(player_hand['values']) > 21:
            if 11 in player_hand['values']:
                player_ace = player_hand['values'].index(11)
                player_hand['values'][player_ace] = 1
        #_____________________________________________________
        # Standard game loop
        if sum(player_hand['values']) < hold_threshold:
            # Instant loss check
            if sum(dealer_hand['values']) != 21:
                # Draw new card
                deal_card(shoe_deck, player_hand)
            #_____________________________________________________
            # Dealer Blackjack
            else:
                draw_live = False
        #_____________________________________________________
        # Limit reachecd       
        else:
            draw_live = False
            
    #_____________________________________________________
    # Dealer's draw logic
    dealer_play(shoe_deck, dealer_hand)
            
    return player_hand, dealer_hand

# Stage 3: Initial deck build <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
# generating new shoe in NDO
ndo_shoe = new_multi_deck()
    
# randomizing order
shoe_deck = randomized_shuffling(ndo_shoe)

# standard interlaced shuffle for further randomization
shoe_deck = interlaced_shuffling(shoe_deck)

# initializing discard deck
discard_deck = new_deck()

# Results bin
win_rates = {"PJDL":0, #Player blackjack, dealer lost
             "PJDB":0, #Player blackjack, dealer bust
             "PLDJ":0, #Player lost, dealer blackjack
             "PJDJ":0, #Push, each with blackjacks
             "PWDL":0, #Player wins, dealer lost
             "PWDB":0, #Player wins, dealer bust
             "PLDW":0, #Player lost, dealer wins
             "PBDW":0, #Player bust, dealer wins
             "PBDB":0, #Player bust, dealer bust
             "PpDp":0, #Standard Push
             "Errors":0} #Error Check

round_messages = {"PJDL": "Lucky you! You got a winning Blackjack!",
                  "PJDB": "Lucky you! You got a winning Blackjack, and the dealer busted!",
                  "PLDJ": "Dealer was dealt a blackjack. Better luck next round.",
                  "PJDJ": "Both you and the dealer were dealt blackjacks. This round is a draw.",
                  "PWDL": "Great job! You beat the dealer with {player_hand_text}!",
                  "PWDB": "Great job! The dealer bust, so your hand of {player_hand_text} wins.",
                  "PLDW": "Better luck next round. The dealer managed to beat you with {dealer_hand_text}.",
                  "PBDW": "You went bust, so the dealer's hand of {dealer_hand_text} won this round. Better luck next round.",
                  "PBDB": "So close! Both you and the dealer went over 21.",
                  "PpDp": "So close! This round is a draw. Both you and the dealer got {dealer_sum}."}

# Stage 4: Option Tree <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
turn_options_1 = {'turn_input': 0, #___Turn_Bins_1___
                  'turn_valid_1': ['S','H','T','D','F'], #(S)tand, (H)it, spli(T), (D)ouble, (F)old
                  'turn_message_1': 'Do you want to (S)tand, (H)it, spli(T), (D)ouble, (F)old?  ',
                  'turn_help': ['Your options are:',
                                'S = Stand, which means to end your turn without drawing another card.',
                                'H = Hit, which means to drawing another card.',
                                'T = Split, which means you can seperate a hand of 2 identical cards into 2 seperate plays on turn 1.',
                                'D = Double, which means to double your bet and draw 1 last card on turn 1.',
                                'F = Fold, which means you take half of your bet back and quit turn 1.'],
                  'turn_default': 'S'}
#_____________________________________________________
turn_options_2 = {'turn_input': 0, #___Turn_Bins_2___
                  'turn_valid_2': ['S','H','D','F'], #(S)tand, (H)it, (D)ouble, (F)old
                  'turn_message_2': 'Do you want to (S)tand, (H)it, (D)ouble, (F)old?  ',
                  'turn_help': ['Your options are:',
                                'S = Stand, which means to end your turn without drawing another card.',
                                'H = Hit, which means to drawing another card.',
                                'D = Double, which means to double your bet and draw 1 last card on turn 1.',
                                'F = Fold, which means you take half of your bet back and quit turn 1.'],
                  'turn_default': 'S'}
#_____________________________________________________
turn_options_3 = {'turn_input': 0, #___Turn_Bins_3___
                  'turn_valid_3': ['S','H'], #(S)tand, (H)it
                  'turn_message_3': 'Do you want to (S)tand, (H)it?  ',
                  'turn_help': ['Your options are:',
                                'S = Stand, which means to end your turn without drawing another card.',
                                'H = Hit, which means to drawing another card.'],
                  'turn_default': 'S'}
#_____________________________________________________
play_options = {'play_input': 0, #___Round_Bins___
                'play_valid': ['Y','N'], #(Y)es, (N)o
                'play_message': 'Do you want to continue playing: (Y)es or (N)o?  ',
                'play_help': ['Your options are:',
                               'Y = Yes, as in to play another round.',
                               'N = No, as in to stop playing.'],
                'play_default': "N"}
#_____________________________________________________
mode_options = {'mode_input': 0, #___Mode_Bins___
                'mode_valid': ['A', 'M'], #(A)uto, (M)anual
                'mode_message': 'Do you want to use the (A)uto or (M)anual play mode?  ',
                'mode_help': ['Your options are:',
                              'A = Automated, which is mainly used for mass analysis. Program will "Hit" until the deck meets a given threshold.',
                              'M = Manual, which allows you to use this more as a standard blackjack game.'],
                'mode_default': 'A'}
#_____________________________________________________
skill_options = {'skill_input': 0, #___Skill_Bins___
                 'skill_mode': ['B','P'], #(B)asic, (P)ro
                 'skill_text': ('Do you want use (B)asic or (P)ro Mode?  '),
                 'skill_help': ['Your options are:',
                                'B = Basic, which simplifies the hands in play to the sum values.',
                                'P = Pro, which allows you to see the face and suit of the cards in play.'],
                 'skill_default': 'B'}
#_____________________________________________________
result_options = {'result_input': 0, #___Result_Bins___
                  'result_valid': ['D','S'], #(D)etailed, (S)implified
                  'result_text': 'Do you want to (D)etail or (S)implified Results?  ',
                  'result_help': ['Your options are:',
                                  "D = Detailed, meaning only percentage results are displayed when you've finished playing.",
                                  'S = Simplified, which shows all outcomes by category along with generalized percentages.'],
                  'result_default': 'S'}
#_____________________________________________________
hold_options = {'hold_input': 0, #___Auto_Bins___
                'hold_valid': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], # Values 1-21
                'hold_text': 'What would you like the player limit to be (dealer holds at 17)?  ',
                'hold_help': ['Your options are:',
                              'Any value between 1 and 21.',
                              'The minimum value of any hand is 2, so 1 would result in standing with whatever is dealt.',
                              'The maximum value of a hand before going bust is 21, so using this would mean go for perfection or go bust.'],
                'hold_default': 17}
#_____________________________________________________
round_options = {'round_input': 0, #___Round_Bins___
                 'round_valid': [True,False],
                 'round_text': 'How many games/rounds do you want simulated?  ',
                 'round_help': ['Your options are:',
                                "Any whole positive integer.",
                                "It's best to start small, and try larger batches depending on how your PC is able to handle the program."],
                 'round_default': 100}
#_____________________________________________________


# Stage 5: Option Selection Set <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________

# ___Input_Tree___
# > Mode #(A)uto, (M)anual

# >> __Auto_Path__
# >> Hold #int(1-21)
# >>> Round #int(any)
# >>>> Result #(D)etailed/(S)implified

# >> __Manual_Path__
# >> Skill #(B)asic/(P)ro
# >>> Result #(D)etailed/(S)implified
# >>>> Turn #(S)tand/(H)it/spli(T)/(D)ouble/(F)old
# >>>>> Play #(Y)es/(N)o

# initial input
mode_options = input_loop(mode_options)
#print(testy_besty)

# auto mode inputs
if mode_options['mode_input'] == 'A':
    hold_options = input_loop(hold_options)
    line_break()
    round_options = input_loop(round_options)
    line_break()
    result_options = input_loop(result_options)
    line_break()

# manual mode settings
else:
    skill_options = input_loop(skill_options)
    line_break()
    result_options = input_loop(result_options)
    line_break()

# Stage 6: Game Loop <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
# randomly picks a shuffle trigger between the first and last 50 cards
cut_target = random.randint(49,(len(shoe_deck['suits']) - 51))
# Initial Setup
shuffle_trigger = False
shuffle_count = 0

#_____________________________________________________
# Auto Check
if mode_options['mode_input'] == 'A':
    for round in range(round_options['round_input']):
        #_____________________________________________________
        # Shuffle if trigger updated
        if shuffle_trigger:
            # reassemble + shuffle deck
            shoe_deck, discard_deck = rotary_shuffling(shoe_deck, discard_deck)
            # generate new cut target
            cut_target = random.randint(49,(len(shoe_deck['suits']) - 51))
            # reset bin
            shuffle_trigger = False
        
        # Shuffle next round if cut target is reached
        if len(shoe_deck['suits']) <= cut_target:
            shuffle_trigger = True
        #_____________________________________________________  
        # Auto play
        player_hand, dealer_hand = deal_loop_auto()
        
        # Results Update
        round_results(player_hand, dealer_hand, win_rates)
        #_____________________________________________________     
        # Player reset
        ace_reset(player_hand)
        discard_transfer(player_hand, discard_deck)

        # Dealer reset
        ace_reset(dealer_hand)
        discard_transfer(dealer_hand, discard_deck)
#_____________________________________________________
# Manual Selection
else:
    new_round = True
    new_game_valid = ["Y","N"]
    
    while new_round:
        #_____________________________________________________
        # Shuffle if trigger updated
        if shuffle_trigger:
            # reassemble + shuffle deck
            shoe_deck, discard_deck = rotary_shuffling(shoe_deck, discard_deck)
            # generate new cut target
            cut_target = random.randint(49,(len(shoe_deck['suits']) - 51))
            # reset bin
            shuffle_trigger = False
            print("Deck shuffled.")
        
        # Shuffle next round if cut target is reached
        if len(shoe_deck['suits']) <= cut_target:
            shuffle_trigger = True
            print("Cut-Card drawn. Deck to be shuffled next round.")
        #_____________________________________________________ 
        # Manual play
        player_hands, dealer_hand = deal_loop_manual()
        
        # Results Update
        for hand in range(len(player_hands)):
            win_rates_copy = copy.deepcopy(win_rates)
            round_results(player_hands[hand], dealer_hand, win_rates)

            # After updating, determine if any changes occurred and print the corresponding message
            for key in win_rates:
                if win_rates_copy[key] != win_rates[key]:
                    # Format and print the appropriate message
                    player_sum = sum(player_hands[hand]['values'])
                    dealer_sum = sum(dealer_hand['values'])

                    if skill_options['skill_input'] == "P":
                        player_hand_text = player_hands[hand]['suits']
                        dealer_hand_text = dealer_hand['suits']
                    else:
                        player_hand_text = player_sum
                        dealer_hand_text = dealer_sum

                    print(round_messages[key].format(player_hand_text=player_hand_text, dealer_hand_text=dealer_hand_text, dealer_sum=dealer_sum))
                    break  # Once the correct message is found, exit the loop
        #_____________________________________________________     
        # Player reset
        for hand in range(len(player_hands)):
            ace_reset(player_hands[hand])
            discard_transfer(player_hands[hand], discard_deck)
            
        # Dealer reset
        ace_reset(dealer_hand)
        discard_transfer(dealer_hand, discard_deck)
        #_____________________________________________________
        # new round check
        new_game_check = input('Would you like to play another round? (Y)es or (N)o? ').upper()
        while new_game_check not in new_game_valid:
            print('Sorry, that was an invalid response. Please respond with a single letter.')
            new_game_check = input('Would you like to play another round? (Y)es or (N)o? ')
        if new_game_check == "N":
            new_round = False
            print("Thank you for playing. Here's how you did this round:")
            line_break()
        else:
            line_break()

# Stage 7: Final Result Print <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
#_____________________________________________________
# Calculating sum of results
total_plays = 0
for key in win_rates:
    total_plays += win_rates[key]
    
print(f'Number of rounds played: {total_plays}')
print('')
#_____________________________________________________
# Detailed Breakdown Check
if result_options['result_input'] == "D":
    print(f"Player blackjack, dealer lost = {win_rates['PJDL']}")
    print(f"Player blackjack, dealer bust = {win_rates['PJDB']}")
    print(f"Player lost, dealer blackjack = {win_rates['PLDJ']}")
    print(f"Push, each with blackjacks = {win_rates['PJDJ']}")
    print(f"Player wins, dealer lost = {win_rates['PWDL']}")
    print(f"Player wins, dealer bust = {win_rates['PWDB']}")
    print(f"Player lost, dealer wins = {win_rates['PLDW']}")
    print(f"Player bust, dealer wins = {win_rates['PBDW']}")
    print(f"Player bust, dealer bust = {win_rates['PBDB']}")
    print(f"Standard Push = {win_rates['PpDp']}")
    #print(f"Error Count = {win_rates['Errors']}")
    line_break()
#_____________________________________________________
# Calculating categories
win_rate = (win_rates['PJDL']+
            win_rates['PJDB']+
            win_rates['PWDL']+
            win_rates['PWDB'])
push_rate = (win_rates['PJDJ']+
             win_rates['PpDp'])
loss_rate = (win_rates['PLDJ']+
             win_rates['PLDW']+
             win_rates['PBDW']+
             win_rates['PBDB'])
#____________________________________________________
# Standard Percentage Breakdown
print(f"Win Rate = {(win_rate/total_plays)*100}%")
print(f"Push Rate = {(push_rate/total_plays)*100}%")
print(f"Loss Rate = {(loss_rate/total_plays)*100}%")

# Bug check deck length (416 = good)
#print(len(discard_deck['suits']))
#print(len(shoe_deck['suits']))a
