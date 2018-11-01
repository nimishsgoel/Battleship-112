# Battleship-112
This repositoroy contains the files that work together to create a battlehip game 
with single player and online multiplayer capabilites. It contains some python files, text files and 
gif files that are used as images in the game.

The following is a small description of the python files:

main - This initializes the game and takes care of most of the front end work.

offline - This has the code for the offline multiplayer code (only 2 can play at a time).

online - This has the code for the online multiplayer code and it uses sockets to achieve it.

single - This has the code for the single player mode, where a player plays against the "computer" which uses
         probability density and memory of previous games to attack the ships.

tp_server - This is the code for the main server that enables the online multiplayer mode
