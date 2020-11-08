# A Two-Way Messagin Bot for Telegram

This bot can be used to communicate between people and a group chat similarly to a share email box. 

The way it works is that a private message sent to the bot is anonymously forwarded to a group chat. If in the group chat someone replys to the forwarded message, the reply is forwarded back to the original sender, again anonymously.

## Usage

### Setting up with BotFather

* Set-up a bot using [BotFather](https://t.me/botfather) and receive a bot token.
* In BotFather set the privacy mode such that the bot has access to all messages by `/help -> /setprivacy -> Disable`.
* Set-up a group chat and add your bot.

### Clone repo and install libraries

```
git clone https://github.com/saskivi/telegram-messaging-bot.git
cd telegram-messaging-bot

virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Finalize set-up

Save the bot token you received from BotFather as an environment variable and create a placeholder environment variable for the chat ID by opening `~/.profile` in a text editor and adding the following lines:
```
export BOT_TOKEN="[the token you received from BotFather]"
export CHAT_ID="0"
```

Update the environment variables and start the bot.
```
source ~/.profile
python telegram-messaging-bot.py
```

Got to the group chat and type `\whoami`. The bot should reply with your chat's ID.

Edit `~/.profile` again and replace the placeholder with the actual chat ID:
```
export CHAT_ID="[ID received from the bot]"
```

Update the environment variables and start the bot again.
```
source ~/.profile
python telegram-messaging-bot.py
```

I recommend running the bot on a server in a terminal window for example using Tmux.

Now everything should work. Test the bot by sending it a private message and replying to it from the group chat.
