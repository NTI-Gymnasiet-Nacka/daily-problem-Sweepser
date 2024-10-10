
import discord
from discord.ext import commands

    
   

TOKEN = 'BOT TOKEN' #This is the token needed for the bot to work

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

TARGET_CHANNEL_ID = "Paste your channel id" # The channel id for ur discord bot

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!') # Prints a message in the terminal when the bot is connected

@bot.event
async def on_message(message):
    
    if message.author == bot.user: # Makes sure it doesnt respond to its own messages
        return

    if message.channel.id != TARGET_CHANNEL_ID: # If the channel isnt in the targeted channel it wont send anything
        return

    content = message.content.lower() # content is whatever you type in discord
    words = content.split()  # Splits all the words

    num1 = None # The price i bought an item for 
    num2 = None # The Price i sold it for 
    first_message = str(words[0])
    Word = first_message
    save_item_name_to_file(Word)  


  
    for i in range(1, len(words)): # This is just a tax calculator
        try:
            num = float(words[i])
            if num1 is None:
                num1 = num
            else:
                num2 = num - 0.025 * num - 0.01 * num
        except ValueError:
            continue
    
    if num1 is not None and num2 is not None: # The bot sends out how much profit i would've made
        result = num2 - num1
        embed = discord.Embed(title=f"Profit from {first_message}\n", description=f"{result:.2f}\n")
        await message.channel.send(embed=embed)
        save_profit_to_file(result) # Saves the profit to a file 
        
        
        
    elif "total" in content.lower(): # if i type in total i will get all profit i've made combined into 1 big number
        total_profit = read_total_profit()
        embed = discord.Embed(title="Total profit", description=f"{total_profit:.2f}")
        await message.channel.send(embed=embed)
    
    elif "reset" in content.lower(): # If i type reset it resets the profit file
        reset()
        embed = discord.Embed(title="Profit reset", description="Profit file has been reset")
        await message.channel.send(embed=embed)
        
    elif "removeitems" in content.lower(): # if i type remove items it removes the item name file
        remove_items()
        embed = discord.Embed(title="Items reset",description="item file has been reset")
        await message.channel.send(embed=embed)
    
    
    elif "list" in content.lower(): # If i type list i a get a list on all the flips and the profit i've made from each item
        
        file1 =open('itemname.txt')
        content = file1.readlines()
        
        file2=open('profit.txt')
        content2=file2.readlines()
       
       
        b=0
        embed = discord.Embed(title="List of items", description="")
        for i in range(0,len(content)):
            embed.add_field(name=" ",value=f"**{content[0+b].rstrip()}**    **{content2[0+b]}**",inline=False)
            b+=1
        await message.channel.send(embed=embed)
    


        
    
        
            
            



def save_item_name_to_file(Word): # Saves the item name to a file
    try:
        with open("itemname.txt", "a") as file:
            if Word is None or Word.strip() == "":
                print("Cannot save empty item name.")
                return
            
            if Word in ["total", "removeitems", "list", "reset"]: # if any of the commands are given it wont save them to the file 
                print(f"Cannot save '{Word}' as it's a special command.")
            else:
                file.write(f"{Word}\n")
                print("Item name saved to file.")
    except IOError as e:
        print(f"Error saving item name to file: {str(e)}")
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        
        
def save_profit_to_file(profit): # This is what saves all the profits to 1 file
    try:
        with open("profit.txt", "a") as file:
            file.write(f"{profit:.2f}\n")
        print(f"Profit saved to file.")
    except Exception as e:
        print(f"Error saving profit to file: {str(e)}")

def read_total_profit(): # calculating the total profit of all items
    x=0
    try:
        with open("profit.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                x += float(line.strip())
            return x 
    except FileNotFoundError:
        return 0

def reset(): # This is used to reset the file
    try:
        with open("profit.txt", "w") as file:
            file.write("")
        print("Profit file reset.")
    except Exception as e:
        print(f"Error resetting profit file: {str(e)}")
    
def remove_items(): # This is used to reset the item file
    try:
        with open("itemname.txt","w") as file:
            file.write("")
            print("Item list has been reset")
    except Exception as e:
        print(f"Error resetting list file: {str(e)}")
bot.run(TOKEN)
