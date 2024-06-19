import os
os.environ['PYTHONOPTIMIZE'] = '2'

import hikari
import lightbulb
import json

with open('info.json') as f:
    token = json.load(f)['token']

bot = lightbulb.BotApp(token=token)


bot.load_extensions_from("./extensions")

bot.run(
    status=hikari.Status.IDLE,
    activity=hikari.Activity(
        name="I'm a Minecraft bot!",
        type=hikari.ActivityType.COMPETING
    )
)
