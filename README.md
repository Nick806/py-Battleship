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
def place_ships(table, ships):
    # Your code here
```
Make sure your bot adheres to these function signatures.


To learn more about creating your bot, refer to the detailed guide in [HOW_TO_MAKE_MY_BOT.md](HOW_TO_MAKE_MY_BOT.md). This guide provides step-by-step instructions and some tips.

Get creative, have fun, and share your bot creations with the community! Everyone is welcome to join the excitement of bot development.

## TODO

- [x] Write the program in english **(most of it)**
- [ ] Add the possibilities to choose between different game modes
- [x] Separate the "main" program from the "bot" porgrams **(made the program more slow)**
- [ ] Make functions more optimized
- [ ] Write some documentation
- [ ] Write the file: "HOW_TO_MAKE_MY_BOT.md"
- [ ] Add a file with the icons (like "X", "O" etc.) and make a function that allow to change it from the program
- [ ] Add the possibility to choose what data is printed
- [ ] Add a gui, perhaps using "pygame"
