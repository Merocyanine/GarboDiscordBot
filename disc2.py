import discord
from prettytable import PrettyTable
from discord.ext import commands
from tabulate import tabulate
import pandas as pd

boot = commands.Bot(command_prefix = '!')


x = PrettyTable()
df = pd.read_csv("example.csv")
users = list(df.columns[1:5]) 

df.fillna("-", inplace = True)

detect_user = False


def add_user(new_user):
    global detect_user
    detect_user = True
    df[new_user] = None
    df.fillna("-", inplace = True)
    df.to_csv("example.csv", index = False)

@boot.event
async def on_ready():
    print("Loading UP")

@boot.event
async def on_command_error(ctx, error): 
    if isinstance(error, commands.MissingRequiredArgument): 
        await ctx.send("Give me another input to complete")


@boot.command(pass_context=True)
async def rate(ctx, arg1, arg2):
    trueauthor = str(ctx.author)[:-5]    
    movies = list(df["Movies"])
    movies_lower_insenstivie = [x.lower() for x in movies]
    movie_whitespacegone = [x.strip() for x in movies]
    if arg1 in movies:
        
        if (trueauthor in users) and (float(arg2) < 11):
            
            if float(arg2):
                authorcolumn = df[trueauthor]
                moviecolumn = df["Movies"]
                index_movie = movies.index(arg1)
                df.loc[index_movie, trueauthor] = str(arg2)
                df.to_csv("example.csv", index = False)
                await ctx.send("Updated Rating!")  
            elif int(arg2) < 0: 
                await ctx.send("No negative numbers")
            else: 
                await ctx.send("Send the movie in full quotes")
        
        else:
            await ctx.send("Choose a rating lower than 10")
        

    elif arg1 in movies_lower_insenstivie: 
        if (trueauthor in users) and (float(arg2) < 11):
            if float(arg2): 
                authorcolumn = df[trueauthor]
                moviecolumn = df["Movies"]
                arg1 = arg1.capitalize()
                index_movie = movies.index(arg1)
                df.loc[index_movie, trueauthor] = str(arg2)
                df.to_csv("example.csv", index = False)
                await ctx.send("Updated Rating!")
                
    
            else: 
                #will not reach this part
                await ctx.send("Send the movie in full quotes")
        else:
            await ctx.send("Choose a rating lower than 10")

        
    else: 
        await ctx.send("Not a movie on the list / type spaced out movies in full quotes")


@boot.command(pass_context=True)
async def add(ctx, *, arg):
    trueauthor = str(ctx.author)[:-5]
    if trueauthor == "user1":    
        if len(str(arg)) < 14:
            users = list(df.columns[1:]) 
            dash = "-" * (len(users))
            dash = list(dash)
            dash.insert(0, arg)
            df.loc[-1] = dash  
            await ctx.send("Added movie to list")
            df.to_csv("example.csv", index = False)

        else:
            await ctx.send("Too long try again")
    else: 
        await ctx.send("Only the author can add movies")    


@boot.command(pass_context=True)
async def movie(ctx):
    embed = discord.Embed(title='Movie Rating')
    await ctx.send(embed=embed)

    df = pd.read_csv("example.csv")
    x.clear()
    movies = list(df["Movies"])
    x.field_names = list(df.columns)
    for l in range(0, len(movies)): 
        x.add_row(list(df.loc[l]))    
        
    l = ("```" + str(x) + "```")
    await ctx.send(l)


@boot.command(pass_context=True)
async def avg(ctx): 
    df = pd.read_csv("example.csv")
    movies = list(df["Movies"])
    ratings_of_everyone = []
    
    for l in range(0, len(movies)):
        n = list(df.loc[l])
        true_numbers = [j for j in n if isinstance(j, float)]
        average = sum(true_numbers)/len(true_numbers)
        ratings_of_everyone.append(average)

    df = pd.DataFrame({"Movies" : movies, "Average" : ratings_of_everyone})
    df.set_index("Movies", inplace=True)
    table = tabulate(df, headers="keys", tablefmt="pretty")
    avg_String =  ("```" + str(table) + "```")
    await ctx.send(avg_String)
    

@boot.command(pass_context=True)
async def logout(ctx):
    return await boot.logout()

boot.run("token")
