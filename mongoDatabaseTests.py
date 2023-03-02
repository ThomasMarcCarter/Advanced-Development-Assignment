import pytest
from pymongo import MongoClient

client = MongoClient('mongodb+srv://tc1301:Superses2@cluster0.nrl5wjb.mongodb.net/?retryWrites=true&w=majority')
db = client['ADUnit']
games = db['testdatabase']

# function that we want to test
def add_game_to_database(game):
    result = games.insert_one(game)
    return result.acknowledged

# unit test
def test_game_to_database():
    #define the game 
    game = {
        'gameTitle': 'PUBG',
        'coverArt': 'https://firebasestorage.googleapis.com/v0/b/ad-project-afc20.appspot.com/o/img%2FPubg-920x518.png?alt=media&token=c249fdc7-329e-41a9-acd3-8a68a60ab7d9',
        'price': '12.99'
    }
    #add the game
    result = add_game_to_database(game)
    assert result == True



# function that we want to test
def remove_game_from_database(game):
    result = games.delete_one({'gameTitle':game['gameTitle']})
    return result.acknowledged

# unit test
def test_remove_game_from_database():
    # create a sample game to add to the database
    game = {
        'gameTitle': 'League of Legends',
        'coverArt': 'https://firebasestorage.googleapis.com/v0/b/ad-project-afc20.appspot.com/o/img%2FEGS_LeagueofLegends_RiotGames_S1_2560x1440-ee500721c06da3ec1e5535a88588c77f.jfif?alt=media&token=74e177f2-46b1-4291-8552-9a40a90b958b',
        'price': '12.99'
    }
    # add the game to the database
    add_game_to_database(game)

    # remove the game from the database
    result = remove_game_from_database({'gameTitle': 'League of Legends'})
    assert result == True

    # check that the game was successfully removed
    game = games.find_one({'gameTitle': 'League of Legends'})
    assert game == None



    # function that we want to test
def replace_game_in_database(game):
    result = games.replace_one({'gameTitle': game['gameTitle']}, game)
    return result.acknowledged

# unit test
def test_replace_game_in_database():
    # create a sample game to add to the database
    game = {
        'gameTitle': 'Osu!',
        'coverArt': 'https://firebasestorage.googleapis.com/v0/b/ad-project-afc20.appspot.com/o/img%2FOsu.jpg?alt=media&token=b6cf9230-70ac-4d6b-b1f1-58d5f42c38ce',
        'price': '0.00'
    }
    # add the game to the database
    add_game_to_database(game)

    
    # create an updated version of the game
    updated_game = {
        'gameTitle': 'Osu!',
        'coverArt': 'https://firebasestorage.googleapis.com/v0/b/ad-project-afc20.appspot.com/o/img%2FOsu.jpg?alt=media&token=b6cf9230-70ac-4d6b-b1f1-58d5f42c38ce',
        'price': '2.00'
    }
        # replace the game in the database
    result = replace_game_in_database(updated_game)
    assert result == True

        # check that the game was successfully replaced
    game = games.find_one({'gameTitle': 'Osu!'})
    #remove the '_id' field before comparing previous version of game to current version of game
    game.pop('_id')
    assert game == updated_game