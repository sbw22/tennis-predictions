    ###### Data: UTR singles and doubles ratings, UTR game-differential, first serve percentage, UTR win percentage,
    ###### Opponent UTR, 3 month trend, longest win streak, best win

    ## Done: UTR singles and doubles ratings, UTR game-differential (weighted and non-weighted), first serve percentage, opponent UTR, UTR win percentage, longest win streak
    ## Not Done: 
    ## Maybe: Best win



if __name__ == "__main__":     
    from bs4 import BeautifulSoup
    import requests
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    import time
    import csv
    import json




    website = 'https://www.atptour.com/en/stats/leaderboard?boardType=serve&timeFrame=52week&surface=all&versusRank=all&formerNo1=false'
    path = '/Users/spencerweishaar/Downloads/chromedriver-mac-arm64/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)

    leaderboard = driver.find_element(By.CSS_SELECTOR, 'div.leaderboard')
    table = leaderboard.find_element(By.CSS_SELECTOR, 'table')

    data = dict()
    for row in table.find_elements(By.TAG_NAME, 'tr')[1:]: # Skips the header row
        cells = row.find_elements(By.TAG_NAME, 'td') # get all the cells in the row
        name = cells[1].text
        data[name] = []
        percent = cells[3].text
        changed_percent = float(percent[0:4])
        data[name].append(changed_percent) # Gets the fourth cell in the table row

    # first_serve = []

    driver.quit() # CLOSES A CHROME DRIVER WINDOW




    ### I USED sudo spctl --master-disable TO DISABLE A PROTECTION FOR MACOS, 
    ### THE RE-ENABLING COMMAND IS sudo spctl --master-enable !!!!!!




    ### Importing swingvison players

    sv_data = {
        "Dongyang Yi": [59.5, 67, 3.37, 3.05],
        "Josue Angulo": [59.5, 41, 4.85, 5.09],
        "Divyansh Devnani": [70, 47.5, 4.34, 0],
        "Tianyi Zhao": [51, 51, 2.98, 0],
        "José Fernando Martínez Garrido": [71.5, 70.5, 7.33, 9.45],
        "Alexandre Vita": [61, 63, 7.43, 0],
        "David Janas": [64, 78.5, 6.93, 7.76],
        "Gaston Deferrari": [62, 71, 7.85, 7.60],
        "Paul Buckle": [57, 77.5, 7.25, 0],
        "Oliver Wreford": [63, 66, 6.81, 7.13],
        "Sookja Kang": [43, 54.5, 3.09, 2.04],
        "Mateo Melgar": [75, 71.5, 8.71, 9.04],
        "Noah Sutin": [68.5, 52.5, 9.39, 8.92],
        "Hendrik Te Grotenhuis": [75, 52, 7.89, 7.55],
        "Jaap Postma": [70.5, 57, 8.32, 8.91],
        "Jason Delos Santos": [56.5, 43.5, 3.61, 4.51],
        "Daniel Lloyd": [52.5, 75, 4.08, 6.87],
        "Lisa Kesler": [46, 64.5, 4.41, 4.82],
        "Michael Rizzo": [58.5, 65.5, 5.42, 6.05],
        "Elaine Ikeda": [68.5, 60, 4.25, 0],
        "Francis Chang": [61, 64, 4.67, 5.36],
        "Alex Yoon": [60.5, 80.5, 7.27, 4.97],
        "Jonas Jones Valintin":  [72.5, 39, 8.27, 0],
        "Pierre Tell": [62, 49, 7.76, 0],
        "Bret Michaelsen": [63.5, 49.5, 5.17, 6.06],
        "Khoa Nguyen": [65.5, 65.5, 7.19, 6.49],
    }




    ### Getting UTR ids for both pro and swingvison players

    # Finds utr ids for players

    player_id_data = dict()


    website = 'https://app.utrsports.net/home'
    path = '/Users/spencerweishaar/Downloads/chromedriver-mac-arm64/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)



    wrapper = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'nav-search-wrapper'))
    )
    name = ""
    search_bar = wrapper.find_element(By.CLASS_NAME, 'form-control')


        # try:
    def get_id(i):
        name = i

        search_text = search_bar.get_attribute("value")

        search_bar.send_keys(name)

        search_text = search_bar.get_attribute("value")

        wait = WebDriverWait(driver, 10)

        dropdown = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'globalSearch__globalSearchDropdownContainer__19eIx'))
        )

        player_dropdown = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, 'globalSearch__globalSearchDropdownOption__2me1B'))
        )


        player_id_string = player_dropdown.get_attribute('data-context')

        player_id = player_id_string[26:34]

        player_id = player_id.strip()

        if player_id[-1] == "-":
            player_id = player_id[0:-1]

        player_id = player_id.strip()

        # player_id_data[i] = player_id


        search_bar.send_keys(Keys.COMMAND + "a")
        search_bar.send_keys(Keys.DELETE)
        search_bar.send_keys(Keys.ARROW_LEFT)
        search_bar.send_keys(Keys.COMMAND + "a")
        search_bar.clear()

        return player_id

        # website2 = ""

        #driver2.quit()

        # except:
        #    data[i].append('None')

    for i in data:
        player_id = get_id(i)
        player_id_data[i] = player_id

    '''
    for i in sv_data:
        player_id = get_id(i)
        player_id_data[i] = player_id

    for i in player_id_data:
        print(f"{i}, id = {player_id_data[i]}")
    '''
    
    driver.quit() # CLOSES A CHROME DRIVER WINDOW





    ### Gets UTR profile data from players


    def profile_data(player_id, tries=10):

        for i in range(tries):
            url = f"https://app.universaltennis.com/api/v1/player/{player_id}"

            response = requests.get(url)
            player_utr_info = response.json()
            time.sleep(0.1)

            return player_utr_info

    for i in data:
        player_info = profile_data(player_id_data[i])
        # print(player_info)
        players_singles_utr = player_info["singlesUtr"] 
        players_doubles_utr = player_info["doublesUtr"]
        data[i].append(players_singles_utr)
        data[i].append(players_doubles_utr)

    spencer_info = profile_data('2588520')
    print(spencer_info)




    ### Getting serve speed to pro players



    def speed_finder(name, file_path):
        with open(file_path, 'r') as serve_stats:
            speed_data = csv.reader(serve_stats, delimiter=',')
            next(speed_data) # Skips the header
            for row in speed_data:
                names = name.split(" ")
                last_name = names[-1]
                print(last_name)
                row_names = row[1].split(" ")
                row_last_name = row_names[-1]
                if row_last_name == last_name:
                    #print(f"Name = {name}")
                    #print(row[1])
                    return row[4]




    file_path = 'StatisticsLeaders.csv'
    for i in data:
        kph_speed = 0.0
        try:
            # Try to find the speed data
            return_value = speed_finder(i, file_path)
            if return_value:  # If speed data is found
                kph_speed = float(return_value[0:3])  # Convert to float
                mph_speed = kph_speed / 1.609  # Convert kph to mph
                mph_speed = round(mph_speed, 2)  # Round to 2 decimal places
                data[i].insert(0, float(mph_speed))  # Append the speed
            else:
                data[i].insert(0, "no data?")  # If no data is found
        except:
            # Handle any errors and append "No data?"
            print(f"Error")
            data[i].insert(0, "no data?")



    # Exception as e    

    for i in data:
        print(f"name: {i}")
        print(f"Full list: {data[i]}")
        print(f"First Serve Speed: {data[i][0]} mph")
        print(f"First Serve Percentage: {data[i][1]}%")





    ### Getting swingvision players' UTR ids


    website = 'https://app.utrsports.net/home'
    path = '/Users/spencerweishaar/Downloads/chromedriver-mac-arm64/chromedriver'
    service = Service(executable_path=path)
    driver = webdriver.Chrome(service=service)
    driver.get(website)



    wrapper = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'nav-search-wrapper'))
    )
    name = ""
    search_bar = wrapper.find_element(By.CLASS_NAME, 'form-control')


    for i in sv_data:
        player_id = get_id(i)
        player_id_data[i] = player_id

    for i in player_id_data:
        print(f"{i}, id = {player_id_data[i]}")



    driver.quit() # CLOSES A CHROME DRIVER WINDOW





    ### Appending Swingvison data onto pro data dictionary


    data.update(sv_data)
    for i in data:
        print(f"{i}: {data[i]}")




    ### Gets match data from players


    def match_data(player_id, match_type, year, tries=10):
        params = {
            "type": match_type,
            "year": year,
        }

        for i in range(tries):
            url = f"https://app.universaltennis.com/api/v1/player/{player_id}/results"

            response = requests.get(url, params)
            player_utr_info = response.json()
            time.sleep(0.01)

            return player_utr_info


    def weight_calc(opp_games, player_games, opp_utr, player_utr):

        player_diff = opp_utr - player_utr  # player_diff and opp_diff are the differences between the opponent and player UTRs
        opp_diff = player_utr - opp_utr
        weight = 0.1
        player_weight = (player_diff * weight) + 1.0    
        opp_weight = (opp_diff * weight) + 1.0

        opp_weight = opp_weight + 0.1 if opp_weight > 0 else opp_weight   # 0.1 is added to the weight so wins count more than losses
        player_weight = player_weight + 0.1 if player_weight > 0 else player_weight


        if player_weight < 0.4:    # If statements create the bounds for the weights
            player_weight = 0.4
        if opp_weight < 0.4:
            opp_weight = 0.4
        if player_weight > 1.75:
            player_weight = 1.75
        if opp_weight > 1.75:
            opp_weight = 1.75

    # player_weighted_games and opp_weighted_games are the weights that are multiplied by the games scored by the player and opponent    
        player_weighted_games = player_games * player_weight
        opp_weighted_games = opp_games * opp_weight

        return (player_weighted_games - opp_weighted_games)



    '''
    for i in data:
        player_info = request_func(player_id_data[i])
        # print(player_info)

        singles_utr = player_info[""]
        doubles_utr = player_info["doublesUtr"]
        data[i].append(singles_utr)
        data[i].append(doubles_utr)
    '''

    def player_match_info(name, player_id, match_type, year):

        player_info = profile_data(player_id)
        player_utr = player_info[f"{match_type}Utr"]

        names = name.split(" ")
        last_name = names[-1]




        if player_utr < 1:  # If player doesn't have a utr, exit this function
            return 

        print(f"{name}'s {match_type} stats for {year}")

        if player_utr < 12.01:    # Adds 0.5 to utrs below 12  because all utrs below 12.5 ish round down to nearest whole number (makes utr average out)
            player_utr += 0.5

        print(f"{name}'s UTR: {player_utr}")


        player_info = match_data(player_id, match_type, year)

        # print(player_info)

        # Variables that are calculating game differintial, utrs, and more

        total_player_games = 0.0
        # player_match_total = 0.0
        total_opp_games = 0.0
        # opp_match_total = 0.0
        total_game_diff = 0.0
        total_weighted_diff = 0.0  # weighted game differential
        opp_total_utr = 0.0
        num_of_opps = 0
        draw_counter = 0
        player_wins = 0
        total_matches = 0
        longest_win_streak = 0
        current_win_streak = 0


        total_games = 0.0


        best_win = 0.0  # might not use


        events = player_info["events"]

        # print(events)

        for k in range(len(events)):
            event = events[k]
            tourney = event["draws"]


            for l in range(len(tourney)):
                draw = tourney[l]
                # print(f"draw name: {draw["name"]}")

                results = draw["results"]
                for match in results:

                    player_result = ""
                    opp_result = ""
                    player = ""
                    opp = ""


                    # print(last_name)


                    last_name = last_name.lower()

                    winner1_lastName = match["players"]["winner1"]["lastName"].lower()    # Makes sure last name isn't two words or more long
                    winner1_lastName = winner1_lastName.lower()
                    winner1_names = winner1_lastName.split(" ")
                    if len(winner1_names) != 1:
                        winner1_lastName = winner1_names[-1]

                    loser1_lastName = match["players"]["loser1"]["lastName"].lower()
                    loser1_lastName = loser1_lastName.lower()
                    loser1_names = loser1_lastName.split(" ")
                    if len(loser1_names) != 1:
                        loser1_lastName = loser1_names[-1]

                    if match_type == "doubles":
                        winner2_lastName = match["players"]["winner2"]["lastName"].lower()
                        winner2_lastName = winner2_lastName.lower()
                        winner2_names = winner2_lastName.split(" ")
                        if len(winner2_names) != 1:
                            winner2_lastName = winner2_names[-1]

                        loser2_lastName = match["players"]["loser2"]["lastName"].lower()
                        loser2_lastName = loser2_lastName.lower()
                        loser2_names = loser2_lastName.split(" ")
                        if len(loser2_names) != 1:
                            loser2_lastName = loser2_names[-1]



                    # print(match["players"]["winner1"]["lastName"])




                    if match_type == "doubles":
                        if winner1_lastName == last_name or winner2_lastName == last_name:
                            player_result = "winner"
                            player = "winner1"
                            opp_result = "loser"
                            opp = "loser1"
                        else:
                            player_result = "loser"
                            player = "loser1"
                            opp_result = "winner"
                            opp = "winner1"
                    else:
                        if winner1_lastName == last_name:  
                            player_result = "winner"
                            player = "winner1"
                            opp_result = "loser"
                            opp = "loser1"
                        else:
                            player_result = "loser"
                            player = "loser1"
                            opp_result = "winner"
                            opp = "winner1"



                    ##########################################################################################################
                    # Adds player and opponent games, and calculates game differential

                    if match_type == "doubles":
                        opp_utr1 = match["players"]["loser1"]["myUtrDoubles"]
                        opp_utr2 = match["players"]["loser2"]["myUtrDoubles"]
                        opp_utr = (opp_utr1 + opp_utr2) / 2
                    else:
                        opp_utr = match["players"][opp]["myUtrSingles"]

                    if opp_utr < 12.1:
                        opp_utr += 0.5

                    opp_games = 0
                    # opp_games keeps track of the number of games opponent won in a match
                    player_games = 0
                    # player_games keeps track of the number of games player won in a match
                    sets = match["score"]
                    for i in sets: # move to inside if when you implement weighted games
                        player_games = player_games + sets[i][player_result]
                        opp_games = opp_games + sets[i][opp_result]


                    total_player_games += player_games
                    total_opp_games += opp_games

                    total_games += player_games   # take away EVERYWHERE once issue is resolved
                    total_games += opp_games

                    ##########################################################################################################
                    # Finds top win and total wins


                    if match_type == "doubles":
                        if winner1_lastName == last_name or winner2_lastName == last_name:
                            player_wins += 1
                            current_win_streak += 1
                        else:
                            current_win_streak = 0
                    else:
                        if winner1_lastName == last_name:
                            player_wins += 1
                            current_win_streak += 1
                        else:
                            current_win_streak = 0



                    longest_win_streak = current_win_streak if current_win_streak >= longest_win_streak else longest_win_streak

                    total_matches += 1



                    #print(best_win)


                    ##########################################################################################################
                    # Adds opponent UTR to total sum of all opponent's utrs 

                    if float(opp_utr) > 1.0:

                        match_weighted_diff = weight_calc(opp_games, player_games, opp_utr, player_utr)

                        opp_total_utr =  opp_total_utr + opp_utr
                        num_of_opps += + 1

                        total_weighted_diff += match_weighted_diff
                        # total_game_diff # ?




                        #print("in if")
                    #print(f"{match["players"][opp]["firstName"]} {match["players"][opp]["lastName"]}'s UTR: {opp_utr}")
                    #i = i + 1


                ################################################################################################################

                # Calculates opp's average UTR by dividing the sum of all opponents utr (opp_total_utr) by the total amount of opponents (num_of_opps)


        # opp_avg_utr = "N/A" if opp_total_utr == 0 or num_of_opps == 0 else opp_total_utr/num_of_opps        

        if opp_total_utr == 0 or num_of_opps == 0:
            opp_avg_utr = "N/A" 
        else:
            opp_avg_utr = opp_total_utr/num_of_opps 

        total_game_diff = total_player_games - total_opp_games    # game differential for the year

        win_percentage = player_wins/total_matches  # win percentage for the year

        if opp_avg_utr != "N/A":

            opp_avg_utr = round(opp_avg_utr, 2)

        win_percentage = round(win_percentage*100, 2)

        total_weighted_diff = round(total_weighted_diff, 2)


        #print(f"Number of draws: {draw_counter}")
        print(f"Average opponent UTR: {opp_avg_utr}")
        print(f"Games won: {total_player_games}")
        print(f"Total opponent games won: {total_opp_games}")
        print(f"Game differential of {year}: {total_game_diff}")
        print(f"Weighted game differential of {year}: {total_weighted_diff}")
        print(f"Win/Loss ratio: {player_wins}:{total_matches-player_wins}")
        print(f"Total matches played: {total_matches}")
        print(f"Win percentage: {win_percentage}%")
        print(f"Longest win streak: {longest_win_streak}\n")
        # print(f"Best win of {year}: {best_win}\n")

        print(f"total_player_games = {total_player_games}, total_opp_games = {total_opp_games}")
        print(f"total_games = {total_games}")
        print(f"total matches = {total_matches}")


        return_list = [opp_avg_utr, total_game_diff, total_weighted_diff, win_percentage, longest_win_streak]

        return return_list



    
        # return     # can change where if and return statements are based on if we want data from individual tourneys, draws, careers, etc        
        #print(f"{name}'s game differential: {total_weighted_diff}")

    year = 2024
    match_types = ["singles", "doubles"]

    for person in player_id_data:
        utr_match_info = dict()
        for match_type in match_types:

            print(f"person = {person}, match_type = {match_type}")
            info_of_matches = player_match_info(person, player_id_data[person], match_type, year)
            match_type_string = f"{match_type}"
            utr_match_info[match_type_string] = info_of_matches

            print(f"utr_match_info[match_type] = {utr_match_info[match_type_string]}\n")

        data[person].append(utr_match_info)





    #player_match_info("Spencer Weishaar", 2588520, 'singles', year)
    #player_match_info("Gavin Nichols", 2731923, 'singles', year)
    #player_match_info("Hank Mast", 3182134, 'singles', year)
    #player_match_info("Nicholas Koch", 4446978, 'singles', year)
    #player_match_info("Cole Horton", 4344449, 'singles', year)
    #player_match_info("Cooper Woestendick", 229035, 'singles', year)
    #player_match_info("Spencer Weishaar", 2588520, 'doubles', year)


    # Make sure to replace total_weighted_diff with weighed_doubles_diff and weighted_singles_diff 




    '''
    for i in data:
        print(i)
        print(data[i][4]["singles"])
        print(f"{data[i][4]["doubles"]}\n")
    '''




    ### Printing off Data


    for i in data:
        player = data[i]
        print(i)
        print(f"Serve speed: {player[0]} mph")
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

        print()



    with open("data.json", "w") as file:
        json.dump(data, file)

    

    
    




