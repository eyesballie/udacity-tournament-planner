#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from matches")
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("delete from players")
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("select count(*) from players")
    result = c.fetchall()
    return int(result[0][0])

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into players (name) values (%s)", (name,))
    DB.commit()
    DB.close()
    


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
    DB = connect()
    c = DB.cursor()
    query = '''
    select players.id, players.name, T1.winner_times, T2.total_times
    From players
    left outer join 
    (select players.id, count(*) as winner_times 
    from players join matches 
	    on players.id = matches.winner
    group by players.id) as T1
	    on players.id = T1.id
    
    left outer join 
    (select players.id, count(*) as total_times 
    from players join matches 
	    on players.id = matches.winner or players.id = matches.loser
    group by players.id) as T2
	    on players.id = T2.id
	    
	order by T1.winner_times desc
    '''
    c.execute(query)
    query_result = c.fetchall()
    players = []
    for row in query_result:
        tup = (int(row[0]), str(row[1]), int(row[2] or 0), int(row[3] or 0))
        players.append(tup)
    return players

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute("insert into matches values (%s, %s)", (winner, loser,))
    DB.commit()
    DB.close()
    
 
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
    result = []
    players = playerStandings()
    i = 0
    while i < len(players) - 1:
        id1 = players[i][0]
        name1 = players[i][1]
        id2 = players[i + 1][0]
        name2 = players[i + 1][1]
        tup = (id1, name1, id2, name2)
        result.append(tup)
        i += 2
    return result

