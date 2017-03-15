# Spar.cli

Spar.cli is a Discord bot. It incorperates some fun commands, useful commands, music commands, and has its own branch of moderator commands too.

The command prefix, by default, is set to `;`, though you can change that at any point using the `prefix` command. Don't worry if you forget the prefix for your server - you can always run a command by mentioning the bot.

---

## Adding Spar.cli

The original Spar.cli bot is run by me, `Caleb#2831`. I'm pretty happy with it as is, since I'm pretty secure in my server and database hosting. As such you can invite the bot that *I* run using [this link](https://discordapp.com/oauth2/authorize?client_id=252880131540910080&scope=bot&permissions=469888119). You don't need to give it any permissions you don't want to, but it *does* need all of the permissions it's asking for in order to run all of its commands. It'll tell you if it's unable to run a certain command due to missing permissions.

## Running it yourself

If you *really* want to run it yourself, you defnitely can. You need a version of Python 3.5  or higher to be able to run your own version. Download all of the files, and grab the requirements using pip:
```bash
pip install -r requirements.txt
```

After that, adjust the tokens inside `TokenSheet.json`, and run the bot:
```bash
python _Main.py TOKEN TokenSheet.json
```

