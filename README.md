partychat-lols
==============
This project is a bot and website designed to record "lols" in your partychat group conversations. It keeps a log of all chat messages and identifies links and images mentioned in chat. Images and links can be viewed in the website and contextual messages around these link and images can are displayed.

Setup
-----

Dependencies:

1. Python, Flask, Jinja2, Werkzeug, SleekXMPP
2. MongoDB, pymongo
3. Heroku Account
4. MongoHQ Account

Setting Up the Software:

1. Create a gmail account dedicated to this bot.
2. Invite the bot to the partychat.
3. Log onto the gmail account and accept partychat invitation.
4. Configure the software with the username/password of the gmail account as well, name of the partychat room, and credentials to the MongoHQ database.
5. Start the logger script.
6. Push the site to heroku.
7. Have some lols.

Todo
----

* Add message context to links and images.
* Add Images and Links Tabs
