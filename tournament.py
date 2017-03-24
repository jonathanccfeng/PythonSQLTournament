#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# Implementation by Jonathan Feng

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM matches;")
    cursor.execute("UPDATE players SET wins = 0, losses = 0, matches = 0;") #reset all players records
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("DELETE FROM players;")
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT count(player_id) as player_count from players;")
    player_count = cursor.fetchone()[0]
    db.close()
    return player_count

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    sql = "INSERT INTO players (player_name, wins, losses, matches) VALUES (%s, %s, %s, %s);"
    data = (name, 0, 0, 0)
    cursor.execute(sql, data)
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    cursor = db.cursor()
    sql = "SELECT player_id, player_name, wins, matches FROM players GROUP BY player_id ORDER BY wins DESC;"
    cursor.execute(sql)
    playerStandingsRecords = cursor.fetchall() #return tuple
    db.close()
    return playerStandingsRecords


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cursor = db.cursor()

    sql = "INSERT INTO matches (player_1_id, player_2_id) VALUES (%s, %s);"
    data = (winner, loser)
    cursor.execute(sql, data)

    sql = "SELECT player_id, wins, losses, matches FROM players WHERE player_id = (%s) OR player_id = (%s);"
    data = (winner, loser)
    cursor.execute(sql, data)    

    for row in cursor.fetchall():
        if row[0] == winner: #player_id matches winner id
            winnerInfo = row
            winnerWins = row[1] + 1
            winnerMatches = row[3] + 1
            updateWinner = (winnerWins, row[2], winnerMatches, row[0])
            cursor.execute("UPDATE players SET wins = %s, losses = %s, matches = %s WHERE player_id = %s;", updateWinner)
            cursor.execute("UPDATE matches SET winner = %s WHERE player_1_id = %s OR player_2_id = %s;", (winner, winner, winner))
            print "Updated table 'matches' with winner of player_id: " ,winner
            print "Updated player_id %d with one more win" % winner
        else:
            loserInfo = row
            loserLosses = row[2] + 1
            loserMatches = row[3] + 1
            updateLoser = (row[1], loserLosses, loserMatches, row[0])
            cursor.execute("UPDATE players SET wins = %s, losses = %s, matches = %s WHERE player_id = %s;", updateLoser)
            print "Updated player_id %d with one more loss" % row[0]
       
    db.commit()
    db.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    db = connect()
    cursor = db.cursor()
    offset = 0
    matchingList = []
    sql = "SELECT * from players;"
    playerTableResults = cursor.execute(sql)
    tableInfo = cursor.fetchall()
    tableLength = len(tableInfo)
    for row in tableInfo:
        if tableLength-1 >= offset: #so we don't get a bunch of None's after
            sql = "SELECT player_id, player_name FROM getPlayerTable LIMIT 2 OFFSET %s;"
            cursor.execute(sql, (offset,))
            offset += 2
            playerOneInfo = cursor.fetchone() #first row
            playerTwoInfo = cursor.fetchone() #second row
            if playerOneInfo != None or playerTwoInfo!= None:
                matchTuple = (int(playerOneInfo[0]), playerOneInfo[1], int(playerTwoInfo[0]), playerTwoInfo[1])
                matchingList.append(matchTuple)

    return matchingList


    

    db.close()





