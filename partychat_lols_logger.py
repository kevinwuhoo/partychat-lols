# Code copied from http://sleekxmpp.com/getting_started/echobot.html

import sys
import logging
from optparse import OptionParser
from os import environ
import re
from datetime import datetime
from subprocess import call
import random

from PIL import Image
import sleekxmpp
from gridfs import GridFS
from connect_mongo import connect_db
import pymongo

PARTYCHAT_ROOM = environ["PARTYCHAT_ROOM"]
GMAIL_USERNAME = environ["GMAIL_USERNAME"]
GMAIL_PASSWORD = environ["GMAIL_PASSWORD"]

PARTYCHAT_ROOM = PARTYCHAT_ROOM + "@im.partych.at"

reload(sys)
sys.setdefaultencoding('utf8')

# http://mathiasbynens.be/demo/url-regex
url_regex = re.compile(r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?', re.IGNORECASE)
img_regex = re.compile(r'.*(gif|jpg|jpeg|png|bmp)$')
tag_regex = re.compile(r'(?:^|\s)#(\w+)')

db = connect_db().message
fs = connect_db()
fs["thumbnail.chunks"].ensure_index([("files_id", 1), ("n", 1)])

fs = GridFS(fs, "thumbnail")


class LolBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
            sender = str(msg["from"])
            sender = sender.split("/")[0]

            # Ignore all messages from other users
            if sender == PARTYCHAT_ROOM:

                msg = msg["body"]
                user_start = msg.index("[") + 1
                user_end = msg.index("]")
                msg_start = user_end + 1

                # Parse out username and message
                user = msg[user_start:user_end]
                chat_msg = msg[msg_start:].strip()

                print "%s: %s" % (user, chat_msg)

                # Get all tags
                tags = tag_regex.findall(chat_msg)

                # Get all urls
                all_urls = url_regex.finditer(chat_msg)

                imgs = []
                urls = []
                url_thumbs = []

                # If urls exist, check if they are images
                if all_urls:
                    for is_url in all_urls:
                        url = is_url.group()

                        # If matches imager regex
                        if img_regex.match(url.lower()):
                            imgs.append(url)

                        # If just a url, then render a thumbnail and resize it
                        else:
                            random_filename = '/tmp/'
                            for i in range(20):
                                random_filename += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
                            random_filename += ".png"
                            call("phantomjs rasterize.js '%s' %s" % (url, random_filename), shell=True)
                            img = Image.open(random_filename)
                            # http://stackoverflow.com/questions/7648200/pip-install-pil-e-tickets-1-no-jpeg-png-support
                            img = img.resize((320, 250), Image.BICUBIC)
                            img.save(random_filename)

                            # Upload it to Mongo
                            img_id = fs.put(open(random_filename))
                            urls.append(url)
                            url_thumbs.append(img_id)

                doc = {"user":user, "msg":chat_msg, "time":datetime.utcnow()}

                # Amend with extra attributes if they were found
                if len(tags) > 0:
                    doc['tags'] = tags
                if len(imgs) > 0:
                    doc['imgs'] = imgs
                if len(urls) > 0:
                    doc['urls'] = urls
                    doc['url_thumbs'] = url_thumbs

                db.insert(doc, safe=True)

if __name__ == '__main__':
    # Setup the command line arguments.
    optp = OptionParser()

    # Output verbosity options.
    optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
    optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)

    opts, args = optp.parse_args()

    # Setup logging.
    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    xmpp = LolBot(GMAIL_USERNAME, GMAIL_PASSWORD)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data Forms
    xmpp.register_plugin('xep_0060') # PubSub
    xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
    if xmpp.connect(('talk.google.com', 5222)):

        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
