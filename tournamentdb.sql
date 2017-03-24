-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE IF NOT EXISTS players (player_id SERIAL primary key, 
					player_name TEXT,
					wins INTEGER,
					losses INTEGER,
					matches INTEGER --number of matches played
					);

CREATE TABLE IF NOT EXISTS matches (match_id SERIAL primary key,
					player_1_id INTEGER references players(player_id),
					player_2_id INTEGER references players(player_id),
					winner INTEGER references players(player_id)
					);

CREATE VIEW getPlayerTable as 

SELECT * 
FROM players
ORDER BY wins DESC;
