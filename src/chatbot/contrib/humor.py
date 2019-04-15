import re
from chatbot.chat import ChatResponse
from chatbot.contrib.base import Feature

class SlapbackFeature(Feature):
    """
    feature: <chatbot.contrib.humor.SlapbackFeature object at 0x105568da0> 
      can handle the query: <chatbot.chat.ChatQuery object at 0x1055c04e0>
    Unhandled Error
    Traceback (most recent call last):
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/internet/tcp.py", line 249, in _dataReceived
        rval = self.protocol.dataReceived(data)
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/words/protocols/irc.py", line 2631, in dataReceived
        basic.LineReceiver.dataReceived(self, data)
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/protocols/basic.py", line 572, in dataReceived
        why = self.lineReceived(line)
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/words/protocols/irc.py", line 2644, in lineReceived
        self.handleCommand(command, prefix, params)
    --- <exception caught here> ---
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/words/protocols/irc.py", line 2699, in handleCommand
        method(prefix, params)
      File "/Users/hobs/anaconda3/envs/ircchat/lib/python3.6/site-packages/twisted/words/protocols/irc.py", line 2056, in irc_PRIVMSG
        self.privmsg(user, channel, message)
      File "/Users/hobs/code/python-chatbot/src/chatbot/client.py", line 34, in privmsg
        default_target = query.user['raw'] if query.private else query.channel
    builtins.AttributeError: 'ChatQuery' object has no attribute 'user' 
    """
    match_re = r"slaps %s(.*)"
    
    def handles_query(self, query):
        if re.match(self.match_re % query.bot.nickname, query.query):
            return True
    
    def handle_query(self, query):
        match = re.match(self.match_re % query.bot.nickname, query.query)
        return ChatResponse("slaps %s back%s" % (query.nickname, match.group(1)), action=True)