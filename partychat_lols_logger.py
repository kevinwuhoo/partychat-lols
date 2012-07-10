# Code copied from http://sleekxmpp.com/getting_started/echobot.html

import sys
import logging
from optparse import OptionParser
import re

import sleekxmpp

USERNAME = ""
PASSWORD = ""
PARTYCHAT_ROOM = ""

PARTYCHAT_ROOM = PARTYCHAT_ROOM + "@im.partych.at"

# Python versions before 3.0 do not use UTF-8 encoding
# by default. To ensure that Unicode is handled properly
# throughout SleekXMPP, we will set the default encoding
# ourselves to UTF-8.
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
else:
    raw_input = input

# http://mathiasbynens.be/demo/url-regex
url_regex = re.compile(r'(?:(?:https?|ftp)://)(?:\S+(?::\S*)?@)?(?:(?!10(?:\.\d{1,3}){3})(?!127(?:\.\d{1,3}){3})(?!169\.254(?:\.\d{1,3}){2})(?!192\.168(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)(?:\.(?:[a-z\u00a1-\uffff0-9]+-?)*[a-z\u00a1-\uffff0-9]+)*(?:\.(?:[a-z\u00a1-\uffff]{2,})))(?::\d{2,5})?(?:/[^\s]*)?', re.IGNORECASE)
img_regex = re.compile(r'.*(gif|jpg|jpeg|png|bmp)$')

class LolBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        """
        Process incoming message stanzas. Be aware that this also
        includes MUC messages and error messages. It is usually
        a good idea to check the messages's type before processing
        or sending replies.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['type'] in ('chat', 'normal'):
            # msg.reply("Thanks for sending\n%(body)s" % msg).send()
            sender = str(msg["from"])
            sender = sender.split("/")[0]

            sender == PARTYCHAT_ROOM
            print sender
            print PARTYCHAT_ROOM
            if sender == PARTYCHAT_ROOM:

                msg = msg["body"]
                # print "%s: %s" % (sender, msg)
                user_start = msg.index("[") + 1
                user_end = msg.index("]")
                msg_start = user_end + 1

                user = msg[user_start:user_end]
                chat_msg = msg[msg_start:].strip()

                print "%s: %s" % (user, chat_msg)

                for is_url in url_regex.finditer(chat_msg):
                    url = is_url.group()

                    print url
                    if img_regex.match(url.lower()):
                        print "Is Image"
                    else:
                        print "Is Url"

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

    xmpp = LolBot(USERNAME, PASSWORD)
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
