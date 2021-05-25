import random
import numpy as np
from .database import *
from fastapi import HTTPException

def get_card(current_user,click_index):
    db = get_db()
    # Define score
    click_counter = 0
    
    print(click_index)
    # New game
    if click_index.new_game is True:
        # Define array cards
        card_a = [i for i in range(1,7)]
        card_b = [i for i in range(1,7)]
        # Shuffle card
        random.shuffle(card_a)
        random.shuffle(card_b)
        # Get global best score and your best score
        global_best_counter = get_global_score(current_user)
        resp = create_or_update_cards(current_user, card_a, card_b, click_counter, global_best_counter['your_best_score'])
        return {'result':'newgame','current_click_counter':resp['click_counter'], 'your_best_score':resp['best_click_counter'],'global_best_score':global_best_counter['global_best_score']}
    else:
        cards = get_data_cards(current_user)
        card_a = cards['cards_index_a']
        card_b = cards['cards_index_b']
        click_count = cards['click_counter']

        # Check index cards,Return score, count of click
        if click_index:
            merged_cards = card_a + card_b
            # print("Answer:",merged_cards)
            # Logic compare
            if merged_cards[click_index.click_a] == merged_cards[click_index.click_b]:
                # print(merged_cards[click_index.click_a],":EQ:",merged_cards[click_index.click_b])

                matches_array = [click_index.click_a,click_index.click_b]
                matches_values = merged_cards[click_index.click_a]

                data_matches = get_or_update_matching(current_user,matches_array,matches_values)
                # print("matches data:",len(data_matches['matches_values']))
                # Check matches index complete game
                if len(data_matches['matches_values']) == 6:
                    # Update best score if current less than best score update new
                    if click_count < data_matches['best_click_counter']:
                        resofcounter = update_click_counter(current_user,click_count,True)
                    # Current game score more than User best score
                    else:
                        click_count = data_matches['click_counter']
                        resofcounter = update_click_counter(current_user,click_count,True)
                    return {'result':'correct', 'status':'gameover', 'matches':data_matches['matches_values'], 'current_click_counter':data_matches['click_counter'], 'your_best_score':data_matches['best_click_counter'], 'global_best_score':resofcounter['global_best_score']}
                # Game not complete
                else:
                    click_count += 2
                    # Update score
                    resofcounter = update_click_counter(current_user,click_count,False)
                    return {'result':'correct', 'status':'gameon', 'matches':data_matches['matches_values'], 'current_click_counter':data_matches['click_counter'], 'your_best_score':data_matches['best_click_counter'],'global_best_score':resofcounter['global_best_score']}
            # Logic not compare
            else:
                # print(merged_cards[click_index.click_a],":Not EQ:",merged_cards[click_index.click_b])
                click_count += 2
                resofcounter = update_click_counter(current_user,click_count,False)
                data_matches = get_or_update_matching(current_user,None,None)
                return {'result':'not correct', 'status':'gameon', 'matches':data_matches['matches_values'], 'current_click_counter':data_matches['click_counter'], 'your_best_score':data_matches['best_click_counter'],'global_best_score':resofcounter['global_best_score']}
        raise HTTPException(status_code=400, detail="No click data.")