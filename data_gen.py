import json
import random

def getting_complete_sets(pre_data, complete_data, match_types):

    for i in pre_data:
        player = pre_data[i]
        # print(i)
        # print(player)
    
        if player[0] == "No data?":
            continue
        elif player[2] == 0 or player[3] == 0:
            continue
        
        will_continue = False

        for match_type in match_types:
            dict_string = f"{match_type}"
            if player[4][dict_string] == None:
                will_continue = True
                
        
        if will_continue == True:
            continue

        if player[4]['doubles'][3] < 0.5 or player[4]['singles'][3] < 0.5:
            continue

        complete_data[i] = pre_data[i]


def ran_opp(num1, num2):    # picks a random opperator 
    random_choice = random.random()
    if random_choice >= 0.5:
        return num1 + num2
    else:
        return num1 - num2




def generator(complete_data, match_types, new_data):
    # Generate random numbers
    # subtract and/or add numbers to data sample x amount of times
    # append new data to data set

    extra_counter = 1

    for i in complete_data:   # for loop goes through complete data set, and for each player, generates x amount more sample players
        player = complete_data[i]
        for l in range(50):

            extra_string = f"extra{extra_counter}"

            ran_num = random.random()

            match_data_dict = dict()
            
            # Generating a random stat for each new sample player being added to the dataset 

            serve_speed_change = ran_num * 4.3
            new_serve_speed = ran_opp(player[0], serve_speed_change)
            new_serve_perc = ran_opp(player[1], (ran_num * 3))
            new_singles_utr = ran_opp(player[2], ran_num)
            new_doubles_utr = ran_opp(player[3], ran_num)

            for match_type in match_types:

                match_type_data = player[4][match_type]
                new_opp_avg_utr = ran_opp(match_type_data[0], ran_num)
                game_diff_change = round(ran_num * 1.2)
                new_game_diff = ran_opp(match_type_data[1], game_diff_change)
                new_weighted_game_diff = ran_opp(match_type_data[2], game_diff_change)
                win_percent_change = ran_num * 5
                
                new_win_percent = ran_opp(match_type_data[3], win_percent_change)
                win_streak_change = round(ran_num * 2.8)
                new_win_streak = ran_opp(match_type_data[4], win_streak_change)
                if new_win_streak <= 0:
                    new_win_streak = 1
                '''
                else:
                    new_win_percent = 0.0
                    new_win_streak = 0
                '''
                match_data_dict[match_type] = [new_opp_avg_utr, new_game_diff, new_weighted_game_diff, new_win_percent, new_win_streak]
        

            new_data[extra_string] = [new_serve_speed, new_serve_perc, new_singles_utr, new_doubles_utr, match_data_dict]

            extra_counter += 1



            

        



def main():

    with open("data.json", "r") as file:
        pre_data = json.load(file)
    # print(pre_data)

    complete_data = dict()

    match_types = ["singles", "doubles"]

    year = 2023

    getting_complete_sets(pre_data, complete_data, match_types)

    new_data = dict()
    '''
    for i in complete_data:
        print(i)
        print(complete_data[i])
        print()
    '''

    generator(complete_data, match_types, new_data)

    for i in new_data:
        print(i)
        print(new_data[i])
        print()
    


    with open("new_data.json", "w") as file:
        json.dump(new_data, file)

   


    


    






'''
    # print(f"Serve speed data type: {type(player[0])}")
    print(f"Serve Percentage: {player[1]}%")
    print(f"Singles UTR: {player[2]}")
    print(f"Doubles UTR: {player[3]}")

    for match_type in match_types:
        dict_string = f"{match_type}"
        print(f"######## {dict_string} UTR stats ########")

        if player[4][dict_string] == None:  
            print("No Data")    # If player does not have data for this match type (Maybe Unrated), print "No Data"
        else:
            print(f"Average opponent UTR: {player[4][dict_string][0]}")
                # print(f"Games won: {total_player_games}")
                # print(f"Total opponent games won: {total_opp_games}")
            print(f"Game differential of {year}: {player[4][dict_string][1]}")
            print(f"Weighted game differential of {year}: {player[4][dict_string][2]}")
                # print(f"Win/Loss ratio: {player_wins}:{total_matches-player_wins}")
                # print(f"Total matches played: {total_matches}")
            print(f"Win percentage: {player[4][dict_string][3]}%")
            print(f"Longest win streak: {player[4][dict_string][4]}")
'''


main()