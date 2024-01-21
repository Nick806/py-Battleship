# py-Battleship
Battleship on python, different gamemode and Bot implementation

## Make your bot!

Feel free to experiment, innovate, and contribute by creating your own bot.

To ensure compatibility to the main file, every bot created should include the following two functions:

### take_shot
This function is responsible for managing the bot's attack. You need to implement the logic to decide where to shoot on the opponent's table.

```python
def take_shot(attac_table, remaining_ships):
    # Your code here
    return row, column
```

### place_ships
This function is responsible for placing the bot's ships on its own table.

```python
def place_ships(rows, columns, ships):
    # Your code here
    return table
```
Make sure your bot adheres to these function signatures.


To learn more about creating your bot, refer to the detailed guide in [HOW_TO_MAKE_MY_BOT.md](HOW_TO_MAKE_MY_BOT.md). This guide provides step-by-step instructions and some tips.

Get creative, have fun, and share your bot creations with the community! Everyone is welcome to join the excitement of bot development.

## TODO

- [ ] Make functions more optimized
- [ ] Add multi-threading
- [ ] try use opencl

### Better readability
- [x] Write the program in english **(most of it)**
- [x] Separate the "main" program from the "bot" porgrams **(made the program more slow)**
- [x] Change the "place_ships" to return the table and get in input Rows and columns
### More beautiful
- [x] Add the title
- [x] Add a gui for Human input
- [ ] Add a gui for Human input ship positioning table
- [ ] Add the possibility to choose what data is printed
- [ ] Add a gui, perhaps using "pygame"
- [x] Add better input for the bots
### More functionality
- [ ] Add the possibilities to choose between different game modes
  - [x] Player plays, random ship positioning
  - [x] bot plays, step by step, random ship positioning
  - [x] bot plays in loop (to get the medium score)
  - [x] bot plays in loop (to get the max and min score)
  - [x] bot plays, step by step, player ship positioning
- [ ] Add config file
  - [x] use a .env file
  - [x] Change the icons
  - [x] some default directory and bots
  - [x] number of rows and columns of the game
  - [ ] Choose what data is printed
- [x] Input/output of "ship_positioning_table"
- [ ] Function to validate a "ship_positioning_table"
### Write some documentation
- [x] Add comments on the functions
- [ ] Write the Readme.md
- [ ] Write the file: "HOW_TO_MAKE_MY_BOT.md"
