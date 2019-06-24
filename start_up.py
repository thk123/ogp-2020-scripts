import os

from trello import TrelloClient


def create_trello_client():
    app_key = os.environ['Trello2020AccessKey']
    access_token = os.environ['Trello2020AccessSecret']
    return TrelloClient(
        api_key=app_key,
        api_secret=access_token,
    )


def boot():
    new_client = create_trello_client()
    oxford2020_board = new_client.get_board(os.environ['Trello2020Board'])
    return new_client, oxford2020_board


print("Welcome to Team2020 Script")
client, board = boot()
