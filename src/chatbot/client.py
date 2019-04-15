from twisted.words.protocols import irc
from twisted.internet import protocol
from chatbot.chat import ChatQuery, ChatResponse


class IRCBot(irc.IRCClient):
    
    def __init__(self, settings=None, *args, **kwargs):
        self.settings = settings
        self.features = []
        self.nickname = self.settings['nickname']
        self.channels = self.settings['channels']
        self.password = settings['server_password']
        for feature in self.settings['features']:
            self.features.append(feature)
        print(f'IRCBot().__dict__: {self.__dict__}')
    
    def signedOn(self):
        for channel in self.channels:
            print(f'joining channel: {channel}')
            self.join(channel)
    
    def privmsg(self, user, channel, message, action=False):
        """Upon receiving a message, handle it with the bot's feature set."""
        print(f'recieved private message: {message}')
        query = ChatQuery(user=user, channel=channel, message=message, bot=self, action=action)
        for feature in self.features:
            print(f"feature: {feature} ...")
            # If they query is unaddressed and addressing is required, move to the next feature
            if feature.addressing_required and not query.addressed:
                print(f"{feature} requires addressing so can't handle the query {query}")
                continue
            if feature.handles_query(query):
                print(f'feature: {feature} \n  can handle the query.__dict__: {query.__dict__}')
                default_target = getattr(query, 'user', {}).get('raw', 'unknown_user') if query.private else query.channel
                response = feature.handle_query(query)
                print(f'response.content: {response.content}')
                if response is not None:
                    # if a target it attached to the response, use it
                    target = getattr(response, 'target', default_target)
                    # Send either an action or a message.
                    if response.action:
                        self.describe(target, response.content)
                    else:
                        self.msg(target, response.content)
                # if the feature disallows continuation, stop iterating over features here
                if not feature.allow_continuation:
                    break

    def action(self, user, channel, data):
        self.privmsg(user, channel, data, action=True)


class IRCBotFactory(protocol.ClientFactory):
    protocol = IRCBot
    
    def __init__(self, settings=None, *args, **kwargs):
        self.settings = settings
    
    def clientConnectionLost(self, connector, reason):
        "If disconnected, reconnect."
        connector.connect()
    
    def buildProtocol(self, addr):
        bot = self.protocol(self.settings)
        bot.factory = self
        return bot
        
    def clientConnectionFailed(self, connector, reason):
        print("connection failed: ", reason)