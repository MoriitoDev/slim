import hikari
import lightbulb
import asyncio
import miru

utility = lightbulb.Plugin("Utility")

class HelpView(miru.View):
    def __init__(self, embeds):
        super().__init__(timeout=60)
        self.embeds = embeds
        self.current_embed_index = 0

    @miru.button(label="⬅️", style=hikari.ButtonStyle.PRIMARY)
    async def previous_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.current_embed_index = (self.current_embed_index - 1) % len(self.embeds)
        await ctx.edit_response(embed=self.embeds[self.current_embed_index])

    @miru.button(label="➡️", style=hikari.ButtonStyle.PRIMARY)
    async def next_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.current_embed_index = (self.current_embed_index + 1) % len(self.embeds)
        await ctx.edit_response(embed=self.embeds[self.current_embed_index])

    @miru.button(emoji="🛑", style=hikari.ButtonStyle.SECONDARY, row=1)
    async def stop_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        for item in self.children:
            item.disabled = True
        await ctx.edit_response(components=self)
        self.stop() 
        
    async def on_timeout(self) -> None:  # No arguments other than self
        if self.message:
            await self.message.delete() 

@utility.command()
@lightbulb.command('help', 'Get information about the bot.')
@lightbulb.implements(lightbulb.SlashCommand)
async def help_command(ctx: lightbulb.Context) -> None:
    client = miru.Client(ctx.bot)
    categories = {}
    for command in ctx.bot.slash_commands.values():
        category = command.plugin.name if command.plugin else 'Uncategorized'
        if category not in categories:
            categories[category] = []
        categories[category].append(command)
    
    embeds = []
    for category, commands in categories.items():
        embed = hikari.Embed(
            title=f"{category} Commands",
            description=f"Commands in the {category} category",
            color=hikari.Color.of(0x5299ba)
        )
        
        for command in commands:
            embed.add_field(name=command.name, value=command.description or "No description", inline=False)
        
        embeds.append(embed)
    
    view = HelpView(embeds)
    message = await ctx.respond(embed=embeds[0], components=view.build(), flags=hikari.MessageFlag.EPHEMERAL)
    client.start_view(view)

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(utility)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(utility)