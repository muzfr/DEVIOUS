import discord
import asyncio
import threading
import os
import time
import random  # status.txt rotation (if you wanna change the status js go to the txt file and put in whatever you want.) #
from colorama import Fore, Style, init
init(autoreset=True)

#### made by muz ####
### contact info | @fanciers on discord | discord.gg/says | @reapproved on youtube | @muzfr on github. ###
### for multi tokens, put your tokens in tokens.txt ###

PACKING = False

# are you a skid?
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def splash():
    clear()
    print(f"""{Fore.RED}
██████╗ ███████╗██╗   ██╗██╗ ██████╗ ██╗   ██╗███████╗       
██╔══██╗██╔════╝██║   ██║██║██╔═══██╗██║   ██║██╔════╝       
██║  ██║█████╗  ██║   ██║██║██║   ██║██║   ██║███████╗       
██║  ██║██╔══╝  ╚██╗ ██╔╝██║██║   ██║██║   ██║╚════██║       
██████╔╝███████╗ ╚████╔╝ ██║╚██████╔╝╚██████╔╝███████║       
╚═════╝ ╚══════╝  ╚═══╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝{Style.RESET_ALL}
{Fore.MAGENTA}      @overflying | discord.gg/says{Style.RESET_ALL}

{Fore.CYAN}    Select an option:{Style.RESET_ALL}
{Fore.YELLOW}    [1]{Style.RESET_ALL} Multi Tokens
{Fore.YELLOW}    [2]{Style.RESET_ALL} Single Token
{Fore.YELLOW}    [3]{Style.RESET_ALL} Credits
{Fore.YELLOW}    [4]{Style.RESET_ALL} Exit
""")
def read_lines(file):
    try:
        with open(file, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] {file} not found.")
        return []

def to_ladder_format(text):
    return '\n'.join(word.upper() for word in text.split())

def run_client(token):
    client = discord.Client()
    REACT_USER_ID = None
    REACT_EMOJI = None
    global PACKING
    ROTATE_STATUS = True  # enable status rotation through the txt

    async def status_rotator():
        await client.wait_until_ready()
        while ROTATE_STATUS:
            statuses = read_lines("status.txt")
            if not statuses:
                await asyncio.sleep(10)
                continue
            status_text = random.choice(statuses)
            status_type = random.choice(["playing", "watching", "listening"])

            if status_type == "playing":
                activity = discord.Game(name=status_text)
            elif status_type == "watching":
                activity = discord.Activity(type=discord.ActivityType.watching, name=status_text)
            else:
                activity = discord.Activity(type=discord.ActivityType.listening, name=status_text)

            try:
                await client.change_presence(activity=activity)
            except Exception as e:
                print(f"[Status Rotation Error] {e}")
            await asyncio.sleep(10)

    async def start_packing(channel, user_mention, lines, ladder=False):
        global PACKING
        PACKING = True
        for line in lines:
            if not PACKING:
                break
            msg = f"{user_mention}\n{to_ladder_format(line)}" if ladder else f"{user_mention} {line}"
            await channel.send(msg)
            await asyncio.sleep(0.4)
        PACKING = False

    @client.event
    async def on_ready():
        print(f"\n[🟢] Logged in as: {client.user}")
        print("\n╔═══════════════════════════════════════╗")
        print("║         MUZ V2 LOADED                   ║")
        print("╠═══════════════════════════════════════  ╣")
        print("║ >pack         >packladder   >packend    ║")
        print("║ >death        >court        >lol        ║")
        print("║ >autoreact    >menu         >stream     ║")
        print("║ >playing      >watching     >listening  ║")
        print("║ >clearstatus  >dm           >purge      ║")
        print("║ >spam                                   ║")
        print("╚═══════════════════════════════════════  ╝\n")
        client.loop.create_task(status_rotator())

    @client.event
    async def on_message(message):
        
        nonlocal REACT_USER_ID, REACT_EMOJI
        global PACKING

        if REACT_USER_ID and REACT_EMOJI:
            if message.author.id == REACT_USER_ID or message.author.id == client.user.id:
                try:
                    await message.add_reaction(REACT_EMOJI)
                except Exception as e:
                    print(f"[React Error] {e}")

        if not message.content.startswith(">"):
            return


        args = message.content.split()
        cmd = args[0].lower()
 
        if cmd == ">packend":
            PACKING = False
            await message.channel.send("[📴] Packing ended.")
            
        elif cmd == ">pack" and len(args) >= 2:
            lines = read_lines("pack.txt")
            await start_packing(message.channel, args[1], lines)
        elif cmd == ">packladder" and len(args) >= 2:
            lines = read_lines("pack.txt")
            await start_packing(message.channel, args[1], lines, ladder=True)
        elif cmd == ">death" and len(args) >= 2:
            lines = read_lines("death.txt")
            await start_packing(message.channel, args[1], lines, ladder=True)
        elif cmd == ">court" and len(args) >= 2:
            lines = read_lines("court.txt")
            await start_packing(message.channel, args[1], lines, ladder=True)
        elif cmd == ">lol" and len(args) >= 2:
            lines = read_lines("lol.txt")
            await start_packing(message.channel, args[1], lines, ladder=False)
            
        elif cmd == ">autoreact" and len(args) >= 3:
            mention = args[1]
            emoji = args[2]
            if mention.startswith("<@") and mention.endswith(">"):
                try:
                    user_id = int(mention.replace("<@", "").replace("!", "").replace(">", ""))
                    REACT_USER_ID = user_id
                    REACT_EMOJI = emoji
                    await message.channel.send(f"[muz runs me] Reacting to {mention} and you with {emoji}")
                except:
                    await message.channel.send("[muz runs me] Invalid mention format.")
            else:
                await message.channel.send("[muz runs me] Invalid @mention format.")
        elif cmd == ">purge":
            try:
                deleted = 0
                async for msg in message.channel.history(limit=100):
                    if msg.author.id == client.user.id:
                        try:
                            await msg.delete()
                            deleted += 1
                            await asyncio.sleep(0.3)
                        except Exception as e:
                            print(f"[Purge Error] {e}")
                await message.channel.send(f"[muz runs me] Purged {deleted} messages.", delete_after=3)
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to purge.")
                print(f"[Purge Error] {e}")
        elif cmd == ">spam" and len(args) >= 3:
            spam_text = ' '.join(args[1:-1])
            try:
                amount = int(args[-1])
                for _ in range(amount):
                    await message.channel.send(spam_text)
                    await asyncio.sleep(0.3)
            except:
                await message.channel.send("[muz runs me] Usage: >spam <message> <amount>")
         


        elif cmd == ">avatar":
            if len(message.mentions) > 0:
                user = message.mentions[0]
            else:
                user = message.author  # fallback to self if no mention

            await message.delete()
            await message.channel.send(user.avatar_url)







         
        elif cmd == ">menu":
            menu = """
📜 MUZ V2 | discord.gg/says | @fanciers

packing utility:
>pack @user         - Regular pack from pack.txt
>packladder @user   - Ladder style pack
>packend            - Stops any active packing
>death @user        - Ladder pack from death.txt
>court @user        - Ladder pack from court.txt
>lol @user          - Regular pack from lol.txt

extra utility:
>autoreact @user 😭   - Auto-react to messages from target and you
>stream <text>        - Set streaming status
>playing <text>       - Set playing status
>watching <text>      - Set watching status
>listening <text>     - Set listening status
>clearstatus          - Clear current presence
>dm <message>         - DM all friends with message (batch of 3, 5s delay)
>purge                - Delete last 100 messages
>spam <msg> <amt>     - Spam message x times
>avatar @user         - sends the mentioned users avatar
"""
            await message.channel.send(f"```{menu}```")
            
        elif cmd == ">stream" and len(args) >= 2:
            stream_title = ' '.join(args[1:])
            activity = discord.Streaming(name=stream_title, url="https://twitch.tv/MUZ")
            try:
                await client.change_presence(activity=activity)
                await message.channel.send(f"[muz runs me] Now streaming: **{stream_title}**")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to set stream status.")
                print(f"[Stream Error] {e}")
        elif cmd == ">playing" and len(args) >= 2:
            game = ' '.join(args[1:])
            activity = discord.Game(name=game)
            try:
                await client.change_presence(activity=activity)
                await message.channel.send(f"[muz runs me] Now playing: **{game}**")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to set playing status.")
                print(f"[Playing Error] {e}")
        elif cmd == ">watching" and len(args) >= 2:
            watching = ' '.join(args[1:])
            activity = discord.Activity(type=discord.ActivityType.watching, name=watching)
            try:
                await client.change_presence(activity=activity)
                await message.channel.send(f"[muz runs me] Now watching: **{watching}**")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to set watching status.")
                print(f"[Watching Error] {e}")
        elif cmd == ">listening" and len(args) >= 2:
            listening = ' '.join(args[1:])
            activity = discord.Activity(type=discord.ActivityType.listening, name=listening)
            try:
                await client.change_presence(activity=activity)
                await message.channel.send(f"[muz runs me] Now listening to: **{listening}**")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to set listening status.")
                print(f"[Listening Error] {e}")
        elif cmd == ">clearstatus":
            try:
                await client.change_presence(activity=None)
                await message.channel.send("[muz runs me] Cleared status.")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to clear status.")
                print(f"[Clear Error] {e}")
        elif cmd == ">dm" and len(args) >= 2:
            msg_to_send = ' '.join(args[1:])
            try:
                friends = await client.user.friends()
                if not friends:
                    await message.channel.send("[muz runs me] No friends found on this token.")
                    return

                await message.channel.send(f"[muz runs me] Starting DM to {len(friends)} friends...")
                sent = 0

                for i in range(0, len(friends), 3):
                    batch = friends[i:i+3]
                    for friend in batch:
                        try:
                            await friend.send(msg_to_send)
                            sent += 1
                        except Exception as e:
                            print(f"[DM Error] Couldn’t DM {friend}: {e}")
                    print(f"[+] Sent DMs to {sent} so far...")
                    await asyncio.sleep(5)

                await message.channel.send(f"[muz runs me] Finished. Total DMs sent: {sent}")
            except Exception as e:
                await message.channel.send("[muz runs me] Failed to send DMs.")
                print(f"[DM Error] {e}")
        else:
            await message.channel.send("[muz runs me] Unknown command.")

    try:
        client.run(token, bot=False)
    except Exception as e:
        print(f"[ERROR] Failed to login: {e}")

def main():
    splash()
    choice = input(">> ").strip()

    if choice == "1":
        tokens = read_lines("tokens.txt")
        if not tokens:
            print("No tokens found in tokens.txt")
            return
        for token in tokens:
            threading.Thread(target=run_client, args=(token,)).start()
    elif choice == "2":
        token = input("Paste your token: ").strip()
        run_client(token)
    elif choice == "3":
        print("\n[👑 CREDITS]")
        print("Made by: Muz @overflying")
        print("Discord server: discord.gg/says\n")
    elif choice == "4":
        print("Exiting...")
        exit()
    else:
        print("Invalid option.")
        time.sleep(1)
        main()

if __name__ == "__main__":
    main()


    
