# vroumbot
![vroum](https://img.shields.io/badge/vroum-vroum-FF0000)
![vroum](https://img.shields.io/badge/vroum-vroum-FF9900)
![vroum](https://img.shields.io/badge/vroum-vroum-FFD800)
![vroum](https://img.shields.io/badge/vroum-vroum-00CC00)
![vroum](https://img.shields.io/badge/vroum-vroum-AAAAFF)
![vroum](https://img.shields.io/badge/vroum-vroum-CC00FF)
![vroum](https://img.shields.io/badge/vroum-vroum-CC00FF)

<p align="center">
  <img src="./media/logo.jpg" width=256px">
</p>

Vroumbot is a bot for managing groupchats on Telegram. Basically a famous shitpost, it continues to be an even more famous shitpost, but with some useful management tools sometimes (for example, a karma or reminder system).

<p align="center" style="font-size:32px;">
  <a href="https://trello.com/b/fTqNq2xu/vroumbot-public" target="_blank"><img src="./media/icon.png" height=32px> A public Trello for feedbacks is available!</a>
</p>

## 🏎️ How to use 🏎️
### 👉 Available directly
You can use [@Vroumbot](https://t.me/vroumbot) to test the bot and use it directly.

All the commands should be listed in [List of commands](https://github.com/Amustache/vroumbot/wiki/List-of-commands).

### 👉 Self hosting
1. Need Python 3.7+, python3-venv and Pip 21+.
2. Clone the repo, `cd` into it.
3. `python -m venv ./env; source ./env/bin/activate`
4. `pip install -Ur requirements.txt`
5. `cp secret.dist.py secret.py` and
   - `TOKEN`: [Your @BotFather token](https://core.telegram.org/bots).
   - `ADMIN_ID`: Your admin user ID. Can be the group ID.
   - `TRELLO_API_KEY`, `TRELLO_API_SECRET`, `TRELLO_FEEDBACK_BOARD`, `TRELLO_FEEDBACK_LIST`: If you want to use Trello.
   - `TRELLO_LINK`: link to the Trello.
6. `./main.py` or `python ./main.py`

## 🚗 Contribute 🚗
### 👉 You know how to code
- To add a new functionality, please use the corresponding `module` (e.g., `modules.spam.text` for silly jokes).
- To add a new module, please use the `base.py` file (i.e., add a new `<file>.py` in the `modules` folder, and create a class which inherits from `Base`).
- Either case, don't forget to register your commands in `commandhandlers`!

**Important**: when adding a new command:
- Check that the command name is not already registered.
- Add it in the correct module.
- Add a corresponding `CommandHandler` in `commandhandlers` of the module `__init__`.
- Add a corresponding `self.logger.info`.
- Test it locally.
- Add a description of it in the [wiki entry](https://github.com/Amustache/vroumbot/wiki/List-of-commands).

**Instructions for adding things**:
1. Fork this repo.
2. Do your things.
3. Stash into one commit, title containing any combination of vroum, message stating what you did.
4. Open a PR.

### 👉 You don't know how to code
You can either:
- Open an issue.
- Use /feedback <what you want to have added> directly in the bot.
