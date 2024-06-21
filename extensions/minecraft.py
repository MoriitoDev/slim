import lightbulb
import requests
import time
import hikari
import datetime
import base64
import os
import json

minecraft = lightbulb.Plugin("Minecraft")

@minecraft.command()
@lightbulb.option(name='username', description='The username of the person you want to get the UUID of.', type=str, required=True)
@lightbulb.command('nametouuid', 'This will return the UUID of a Minecraft name')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(ctx: lightbulb.Context) -> None:
    timestamp = int(time.time())
    username = ctx.options.username
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}?at={timestamp}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        uuid = data['id']
        
        embed = hikari.Embed(title='UUID', description=f'The UUID of {username} is {uuid}', color=0x5299ba)
        embed.set_thumbnail(f'https://mc-heads.net/avatar/{uuid}')
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(f"Error: {response.text}")
        
@minecraft.command()
@lightbulb.option(name='username', description='The nickname of the player to get the skin from.', type=str, required=True)
@lightbulb.command('skin', 'This will return the skin of a Minecraft player!')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(ctx: lightbulb.Context) -> None:
    username = ctx.options.username
    timestamp = int(time.time())
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}?at={timestamp}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        uuid = data['id']
    
        embed = hikari.Embed(title='Minecraft Skin', color=0x5299ba, description=f'**Download it [here](https://mc-heads.net/download/{uuid})**')
        embed.set_image(f'https://mc-heads.net/body/{uuid}/right')
        await ctx.respond(embed=embed)
        
    else:
        data = response.json()
        await ctx.respond(f'{data['Error']['errorMessage']}')
        
@minecraft.command()
@lightbulb.option(name='server', description='Server to get status from.', type=str, required=True)
@lightbulb.command('server', 'Get the status of a minecraft server.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(ctx: lightbulb.Context) -> None:   
    link = f"https://api.mcsrvstat.us/3/{ctx.options.server}"
    
    response = requests.get(link)
    
    if response.status_code == 200:
        
        
        data = response.json()
        online = data['online']
        print('Online')
        
        if online == False:
                await ctx.respond('The server you provided is not a known server.', flags=hikari.MessageFlag.EPHEMERAL)
                
        elif online == True:         
        
            hostname = data['hostname']
            version = data['version']
            img = data['icon']
            online_players = str(data['players']['online'])
            max_players = str(data['players']['max'])
            
            embed = hikari.Embed(title=' ```Server Status```', color=0x2c2e47)
            
            embed.add_field(name='```Host Name```', value=hostname, inline=False)
            embed.add_field(name='```Version```', value=version, inline=False)
            embed.add_field(name='```Online Players```', value=online_players + ' / ' + max_players, inline=False)
            embed.set_thumbnail(img)
            await ctx.respond(embed=embed)
            
            
            
        else:
            await ctx.respond(online)
            

@minecraft.command()
@lightbulb.option(name='user', description='The user to get the information from.', type=str, required=True)
@lightbulb.command('hypixel', 'Get the information about a hypixel player.')
@lightbulb.implements(lightbulb.SlashCommand)
async def command(ctx: lightbulb.Context) -> None:  
    
    with open('info.json') as f:
        hypixel_api = json.load(f)['hypixel-api']
                
    player = ctx.options.user
    
    data = requests.get(
        url='https://api.hypixel.net/v2/player',
        params={
            "key": hypixel_api,
            "name": player
        }
        ).json()

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(minecraft)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(minecraft)
