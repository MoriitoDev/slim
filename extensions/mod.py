import lightbulb
import hikari
import time

plugin = lightbulb.Plugin("test")

@plugin.command()
@lightbulb.add_checks(lightbulb.guild_only)
@lightbulb.command('asd', 'Tells you the bot\'s ping')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(ctx: lightbulb.Context) -> None:
    try:
        
        websocket_latency = ctx.bot.heartbeat_latency * 1000  
        start = time.monotonic()
        message = ctx.respond("Pinging...")
        end = time.monotonic()
        api_latency = (end - start) * 1000
        await message.edit(f"Websocket Latency: {websocket_latency}ms\nAPI Latency: {api_latency}ms")
    except Exception as e:
        await ctx.respond(str(e))
    
    
def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)