import re

class ChatQuery(object):
    ADDRESSED_RE = "%s\s*[:,\-]?\s*(.*)"
    
    def __init__(self, **kwargs):
        self.raw_data = kwargs
        self.bot = kwargs['bot']
        self.nickname = kwargs['user'].split('!', 1)[0]
        self.private = True if kwargs['channel'] == self.bot.settings['nickname'] else False
        self.query = kwargs['message']
        self.channel = kwargs['channel']
        self.action = kwargs['action'] if 'action' in kwargs else False
        self.user = dict()
        self.user['raw'] = kwargs['user']
        self.user['name'] = self.user['raw'].split('!', 1)[0]
        self.user['url'] = self.user['raw'].split('!', 1)[-1]
        
        # check if the match is addressed
        addressed_match = re.match(self.ADDRESSED_RE % self.bot.settings['nickname'], self.query)
        if addressed_match:
            self.addressed = True
            self.query = addressed_match.group(1)
        else:
            self.addressed = False
        print(f'ChatQuery().__dict__: {self.__dict__}')


class ChatResponse(object):

    def __init__(self, content, **kwargs):
        self.content = content
        if 'target' in kwargs:
            self.target = kwargs['target']
        self.action = kwargs['action'] if 'action' in kwargs else False
        print(f'ChatResponse().__dict__: {self.__dict__}')
    
    def __str__(self):
        print(f'ChatResponse.__str__(): {self.content}')
        return self.content