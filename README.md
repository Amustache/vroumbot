# vroumbot
![vroum](https://img.shields.io/badge/vroum-vroum-FF0000)
![vroum](https://img.shields.io/badge/vroum-vroum-FF9900)
![vroum](https://img.shields.io/badge/vroum-vroum-FF9900)
![vroum](https://img.shields.io/badge/vroum-vroum-00CC00)
![vroum](https://img.shields.io/badge/vroum-vroum-AAAAFF)
![vroum](https://img.shields.io/badge/vroum-vroum-CC00FF)
![vroum](https://img.shields.io/badge/vroum-vroum-CC00FF)

![vroum](https://cdn4.telesco.pe/file/lLmBw8DlJlP8dzPonc7rwGd4a4-oqn50fw_iIsBRtt5v1Ft4xPxOOWZ4FeqTMZ2KnvBwb3W4n6hfH7EU28fAqFsY6ZA6iR__oLk6mA82QJGz6c-ik-9VLg45dw9LkFowRL2pakZ5DFy4eix8G33XKGaKNSexL6YTCBwfFZFY0YeQKjYO3onfZ5xH2MqGE3onAXLYcRS1kG7pl42qh9VOS3ECz5zvwxtNwugVeY88UJSDpBqfRJN1zusDtKVhNbVNiTAiH3w97Bqm-KbwnFUZ4MUkX39exTtgy97Z6qcsM814TmE1mrxNEsHBIVjboK4lwrLrQwJAmB37VZoCyIkvnw.jpg)

Vroumbot is a bot for managing groupchats on Telegram. Basically a famous shitpost, it continues to be an even more famous shitpost, but with some useful management tools sometimes (for example, a karma or reminder system).

## How to use
### Available directly
You can use [@Vroumbot](https://t.me/vroumbot) to test the bot and use it directly.

### Self hosting
1. Need Python 3.7+, python3-venv and Pip 21+.
2. Clone the repo, `cd` into it.
3. `python -m venv ./env; source ./env/bin/activate`
4. `pip install -Ur requirements.txt`
5. `cp secret.dist.py secret.py`
6. Put your botfather token and your personal chatid in the file `secret.py`, as well as Trello if needed.
7. `./main.py` or `python ./main.py`

## Contribute
### You know how to code
- To add a new functionality, please use the corresponding `module` (e.g., `modules.spam.text` for silly jokes).
- To add a new module, please use the `base.py` file (i.e., add a new `<file>.py` in the `modules` folder, and create a class which inherits from `Base`).
- Either case, don't forget to register your commands in `commandhandlers`!

### Instructions for commits
1. Fork this repo.
2. Do your things.
3. Stash into one commit, title containing any combination of vroum, message stating what you did.
4. Open a merge request.

or

1. New branch.
2. Do your things.
3. Stash into one commit, title containing any combination of vroum, message stating what you did.
4. Open a merge request.

### You don't know how to code
1. Open an issue.

or

1. Use /feedback <what you want to have added> directly in the bot.
