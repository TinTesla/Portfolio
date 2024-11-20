
# dependencies
import random
import pandas as pd

# simplified deck
cards = [2,3,4,5,6,7,8,9,10,10,10,11]
def new_card():
    pick = random.randint(0,11)
    card = cards[pick]
    return card

# Initial setup
full_result = {}
total_plays = 1000000


#loop per card value
for card_1 in range(2,12):
    
    #bin reset
    round_result = {'% end hand 17':0,
                    '% end hand 18':0,
                    '% end hand 19':0,
                    '% end hand 20':0,
                    '% end hand 21':0,
                    '% bust':0,
                    'avg end hand':0}
    
    result_count = {'end hand 17':0,
                    'end hand 18':0,
                    'end hand 19':0,
                    'end hand 20':0,
                    'end hand 21':0,
                    'busts':0,
                    'end hands':[]}
    
    # main loop
    #_______________________________
    for _ in range(total_plays):
           
        #initial hand
        hand = [card_1,new_card()]
        
        # dual ace check
        if sum(hand) == 22:
            dealer_ace = 0 
            hand[dealer_ace] = 1
            
        # deal logic
        if sum(hand) < 17:
            while sum(hand) < 17:
                hand.append(new_card())
                if sum(hand) > 21:
                    if 11 in hand:
                        dealer_ace = hand.index(11)
                        hand[dealer_ace] = 1
                        
        # update inner bins
        if sum(hand) == 17:
            result_count['end hand 17'] += 1
        elif sum(hand) == 18:
            result_count['end hand 18'] += 1
        elif sum(hand) == 19:
            result_count['end hand 19'] += 1
        elif sum(hand) == 20:
            result_count['end hand 20'] += 1
        elif sum(hand) == 21:
            result_count['end hand 21'] += 1
        elif sum(hand) > 21:
            result_count['busts'] += 1

        # add hand to inner bin
        result_count['end hands'].append(sum(hand))

    # update outer dictionary
    round_result['% end hand 17'] = round((result_count['end hand 17']/total_plays)*100,2)
    round_result['% end hand 18'] = round((result_count['end hand 18']/total_plays)*100,2)
    round_result['% end hand 19'] = round((result_count['end hand 19']/total_plays)*100,2)
    round_result['% end hand 20'] = round((result_count['end hand 20']/total_plays)*100,2)
    round_result['% end hand 21'] = round((result_count['end hand 21']/total_plays)*100,2)
    round_result['% bust'] = round((result_count['busts']/total_plays)*100,2)
    round_result['avg end hand'] = round(sum(result_count['end hands'])/total_plays,2)
    
    # push outer dictionary
    full_result[f"dealer shows {card_1}"] = round_result

# Results print
print(f'Based on {total_plays} simulations per:')
df = pd.DataFrame(full_result)
print(df)