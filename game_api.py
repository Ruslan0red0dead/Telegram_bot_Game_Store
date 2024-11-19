# this code performs a keyword search
# The googleapiclient library will help us create a search engine
# requests library is needed for our api

import requests
from googleapiclient.discovery import build


# here you can get api https://developers.google.com/custom-search/v1/introduction
# click on the "Get a Key" button
api_key = 'GIzaSyCAczneS201lYQnPUSZ-JlPRVqes0vCgvI'

# here you can get cse_id https://programmablesearchengine.google.com/
cse_id = '151621wbf1a704a45'

def Api_data(query):
    # found_games is a variable with a list in which the found games will be stored
    found_games = []

    # the service and result variables will scale keywords
    service = build('customsearch', 'v1', developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id).execute()


    # the index_game variable is needed to index games from 1 instead of 0
    # python counts from 0, not from 1
    # so every game found will be indexed
    # this is necessary for beauty and for the bot user to see which game is on the list

    index_game = 1
    for item in result['items']:
        # the response variable contains the api
        # in this bot I used the game store api "steampay"
        response = requests.get(f'https://steampay.com/api/search?query={item["title"]}')

        response_json = response.json()

        for item_2 in response_json['products']:
            # add all found games to the list
            found_games.append([index_game, f"{item_2['url']}"])

            index_game += 1

    return found_games