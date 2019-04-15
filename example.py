# example.py


from chatbot.bots import Bot
from chatbot.contrib import *

bot = Bot(
    nickname = 'nlpia-bot',
    hostname = 'chat.freenode.net',
    port = 6667, # 6665,
    server_password = 'b0tabl31rc',  # /msg nickserv register b0tabl31rc nlpia-bot@totalgood.com
    channels = ('#freenode', '#python', '#bots'),
    features = (
        PyPIFeature(),
        WikipediaFeature(),
        DictionaryFeature(),
        DiceFeature(),
        ChoiceFeature(),
        SlapbackFeature(),
    )
)

bot.run()