import requests
import discord
import os
from prettytable import PrettyTable
from discord.ext import commands
from tabulate import tabulate

boot = commands.Bot(command_prefix = '!')

#table information
x = PrettyTable()
true_users = ["Movies", "momomo", "Eddy", "Shabooby", "Trulicup"]
dic_key = {"momomo": 1, "Eddy": 2, "Shabooby": 3, "Trulicup":4}
x.field_names = true_users
detect_user = False

#adds a new user when called to the table information
def add_user(new_user):
    global detect_user
    detect_user = True
    next_number = len(dic_key) + 1
    dic_key[new_user] = next_number
    true_users.append(new_user)

#On start to alert you
@boot.event
async def on_ready():
    print("Loading UP")


#Discord command that uses two text files that will simultaneously edit each file
#"wt" deletes the entire file so data will be saved in the other file when "rt" and vice versa
#will edit the file into lists, change values acordingly, and finally rejoins | Many layers to an onion
@boot.command(pass_context=True)
async def rate(ctx, arg1, arg2):
    file = open("movielist.txt", "rt")
    fileout = open("output.txt", "wt")

   
    mastermovielist  = []
    #print(fileout)
    for line in file:
        wrr = line.split()
        mastermovielist.append(wrr[0])
    #print(mastermovielist)
    if arg1 in mastermovielist:
        trueauth = str(ctx.author)[:-5]

        if trueauth in true_users:
            #add_movie(trueauth, dic_connection[trueauth])
            #making sure you are the author and adding movielist
        #if trueauth == "momomo": #might not need this TAB this since abstracted now
            file = open("movielist.txt", "rt")
            fileout = open("output.txt", "wt")
            #why do u have to open the file again in this part? :/
            full = []
            for line in file:
                wrr = line.split()
                full.append(wrr)
                mastermovielist.append(wrr[0])
                print(line)
            #Searching through the nested loop
            for sublist in full:
                if arg1 in sublist: #ARGUMENT here if the movie
                    sublist[dic_key[trueauth]] = str(arg2) #sublist[1]
            await ctx.send("Updated Rating!")

            finished = [" ".join(u) for u in full]
            #print(finished)
            #finished2 = [l.strip('[]') for l in finished]
            finished2 = [fileout.write(j + "\n") for j in finished]
            #print(finished2)
            file.close()
            fileout.close()
            file2 = open("movielist.txt", "wt")
            fileout2 = open("output.txt", "rt")
            data2 = fileout2.read()
            file2.write(data2)
            file2.close()
            fileout2.close()

        #else:
            #await ctx.send("No one here is named that, I lazily hard-coded this")
    else:
        add_user(trueauth)
        await ctx.send("Not the correct format, send again")

   


#Discord command here will simply add a movie to the text files. will also detect if a new user has joined and add them accordingly.
@boot.command(pass_context=True)
async def add(ctx, arg):
    basecase = f"{arg} - - - -"
    if len(str(arg)) < 14:
        if detect_user == False:            
            with open("output.txt", 'a') as fin:
                fin.write(f"{arg} - - - -\n")

            with open("movielist.txt", "a") as fin2:
                fin2.write(f"{arg} - - - -")

        elif detect_user == True: 
            newbase = basecase + " -"
            with open("output.txt", 'a') as fin:
                fin.write(f"newbase\n")

            with open("movielist.txt", "a") as fin2:
                fin2.write(f"newbase\n")

        await ctx.send("Added movie to list")
    else:
        await ctx.send("Too long try again")
    


#Discord command that displays the movie
#Same technique as rate command except slicing and dicing to add to the tabulate class
@boot.command(pass_context=True)
async def movie(ctx):
    embed = discord.Embed(title='Movie Rating')
    await ctx.send(embed=embed)

    ####### file extraction

    bang = []
    bang2 = []
    mastermovie = []
    mastermovie2 = []
    with open("output.txt", "r") as file:
        for line in file:
             wrr = line.split()
             mastermovie.append(wrr[0])
             for word in line.split():
                 bang.append(word)
    with open("movielist.txt", "r") as file2:
        for line in file2:
            wrr = line.split()
            mastermovie2.append(wrr[0])
            for word in line.split():
                bang2.append(word)
    #print(mastermovie)
    #print(mastermovie2)
    #if contents of file are same inside each
    #lastfile = open("output.txt", "r")
    #lastfile2 = open("movielist.txt", "r")
    print(bang)
    print(bang2)
    bang.sort()
    bang2.sort()
    mastermovie.sort()
    mastermovie2.sort()
    if bang == bang2:
        beng = []
        x.clear()
        #true_users = ["Movies", "momomo", "Eddy", "Shabooby", "Trulicup"]
        x.field_names = true_users
        with open("output.txt", "r") as file:
            for line in file:
                for word in line.split():
                    beng.append(word)
        data = [beng[x:x+5] for x in range(0, len(beng), 5)]
        final = [x.add_row(i) for i in data]
        l = ("```" + str(x) + "```")
        await ctx.send(l)


    else:
        x.clear()
        bung = []
        #true_users = ["Movies", "momomo", "Eddy", "Shabooby", "Trulicup"]
        x.field_names = true_users
        with open("output.txt", "r") as file:
            for line in file:
                for word in line.split():
                    bung.append(word)
        data = [bung[x:x+5] for x in range(0, len(bung), 5)]
        final = [x.add_row(i) for i in data]
        #print(bung)

        #print(final)
        l = ("```" + str(x) + "```")
        await ctx.send(l)

    author = str(ctx.author)
    finalauth = author[:-5]
    

#simply logouts
@boot.command(pass_context=True)
async def logout(ctx):
    return await boot.logout()


#Future additions: Maybe a delete function? 
#Make sure to comment as more code willl be added by Truli/me

boot.run("token")
