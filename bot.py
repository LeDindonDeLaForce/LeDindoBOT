# bot.py
import asyncio
import logging
import os  # for importing env vars for the bot to use
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import custom_commands
from twitchio import Channel, Client, User
from twitchio.ext import commands, pubsub, routines

from utils import check_for_bot, random_bot_reply, random_reply, auto_so


tw_channels=["type", "each", "channel", "which", "uses", "bot"]


class ledindobot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=os.environ['ACCESS_TOKEN'],
            prefix=os.environ['BOT_PREFIX'],
            initial_channels=tw_channels,
            case_insensitive=True
        )
        self.pubsub_client = None
        self.channel = None
        self._cogs_names: t.Dict[str] = [
            p.stem for p in Path(".").glob("./cogs/*.py")
        ]
        self.vip_so = {
            x: {} for x in tw_channels
        }
        self.bot_to_reply = ['wizebot', 'streamelements', 'nightbot', 'moobot', 'bothagonas', 'nitr0genbot']
        self.giveaway = set()

    def setup(self):
        random.seed()

        logging.info(f'{self._http.client_id}')
        logging.info("Chargement des cogs...")

        for cog in self._cogs_names:
            logging.info(f"Loading `{cog}` cog.")
            self.load_module(f"cogs.{cog}")

        logging.info("Chargement terminé")

    def run(self):
        self.setup()
        super().run()

    async def event_ready(self):
        # Notify us when everything is ready!

        # Subscribes through pubsub to topics
        u: List["User"] = await self.fetch_users(names=[os.environ['CHANNEL']])
        uu: User = u[0]

        topics = [
            #pubsub.channel_points(self.pubsub_client._http.token)[uu.id]
        ]
        #await self.pubsub_client.pubsub.subscribe_topics(topics)
        #await self.pubsub_client.connect()
        self.channel = self.get_channel(os.environ['CHANNEL'])

        # Starting timers
        logging.info("Starting routines...")
        self.links.start()

        # Retrieving custom commands from db
        custom_commands.init_commands()

        # Retrieving routines from db
        self.routines = custom_commands.init_routines(self)
        
        # Retrieving author quotes from db
        custom_commands.init_authors(tw_channels)
        
        # Retrieving stream queues in case of bot crashed or stopped
        custom_commands.init_queue(tw_channels)


        # Initializing Users on database and adding new ones to db automatically
        self.usernames = custom_commands.init_users(tw_channels)


        # We are logged in and ready to chat and use commands...
        logging.info(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot...
        # For now we just want to ignore them...
        if message.echo:
            return

        # Print the contents of our message to console...
        logging.info(
            f'{message.author.name} on channel {message.author.channel.name}: '
            f'{message.content}'
        )

        # if check_for_bot(message.content):
        #     logging.info("BOT DETECTED")
        #     message.author.channel.send(
        #         f'/ban {message.author.name} Vilain Bot')

        if message.content[0] == os.environ['BOT_PREFIX']: # si une custom command est jouée
            reply = custom_commands.find_command(message)
            if reply is not None: #await message.author.channel.send(reply) [custom command sans tag de celui qui l'a jouée]
                await message.author.channel.send(f"@{message.author.name} {reply}") # [custom command avec tag de celui qui l'a jouée]
                return

        if "@ledindobot" in message.content.lower(): #AUTO SO et réponses aléatoires du bot
            await random_reply(self, message)
            #UNCOMMENT LINES BELOW TO RE ENABLE RANDOM BOT REPLY
            
        #elif message.author.name.lower() in self.bot_to_reply:
        #    await random_bot_reply(message)
        #else:
        #    await auto_so(self, message, self.vip_so[message.author.channel.name])

        # Since we have commands and are overriding the default `event_message`
        # We must let the bot know we want to handle and invoke our commands...
        await self.handle_commands(message)

    async def event_raw_usernotice(self, channel, tags):
        logging.debug(tags)
        if tags["msg-id"] == "sub":
            await channel.send(f"/me PogChamp {tags['display-name']} rejoint l'ordre de la plume d'Or! Merci pour le sub PogChamp")
        elif tags["msg-id"] == "resub":
            await channel.send(
                f"/me PogChamp Le resub de {tags['display-name']}!! Merci pour ton {tags['msg-param-cumulative-months']}ème mois <3"
            )
        elif tags['msg-id'] == 'subgift':
            await channel.send(
                f'/me {tags["display-name"]} est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un subgift !'
            )
        elif tags['msg-id'] == 'anonsubgift':
            await channel.send(
                f'/me Un donateur anonyme est vraiment trop sympa, il régale {tags["msg-param-recipient-display-name"]} avec un subgift !'
            )
        elif tags["msg-id"] == "raid":
            await channel.send(
                f"/me LEZ GO OEEE y'a un raid de {tags['msg-param-displayName']} avec {tags['msg-param-viewerCount']} margoulins qu'arrive !"
            )

    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            logging.error("Command does not exist")

    ## PUBSUB FUNCTIONS ##
    async def event_pubsub_channel_points(self, event: pubsub.PubSubChannelPointsMessage):
        logging.info(
            f'Redemption by {event.user.name} of reward {event.reward.title} '
            f'with input {event.input} done'
        )
        if event.reward.title == "Hats off to you":
            minutes = 5
            time = datetime.now() + timedelta(minutes=minutes)
            await self.channel.send(f"/me Met le casque jusqu'à {time.strftime('%H:%M:%S')}")
            await asyncio.sleep(minutes * 60)
            await self.channel.send("/me @Leix34 tu peux maintenant retirer le casque")

        if event.reward.title == "Giveaway":
            logging.info(f'{event.user.name} entered the giveaway!')
            self.giveaway.add(event.user.name)

    ## ROUTINES ##
    @routines.routine(minutes=40.0, wait_first=False)
    async def links(self):
             await self.channel.send("Moi robot MrDestructoid Kappa")
             await asyncio.sleep(60 * 40)
             await self.channel.send("Il se passe un truc incroyable ? Le dindon se fait dindonned ? Lâche un clip, fais toi plaiz ! TTours")
             await asyncio.sleep(60 * 40)
             await self.channel.send("Si le contenu de la chaîne te plaît, hésite pas à follow pour ne pas manquer la suite ledind1Hey")
             await asyncio.sleep(60 * 40)
             await self.channel.send("Mon serveur discord: https://discord.gg/7QyK5U3BKD ImTyping")
             await asyncio.sleep(60 * 40)



    @commands.command(name="routine_add")
    async def routine_add(self, ctx: commands.Context, name, seconds, minutes, hours, *text):
        if not ctx.author.is_mod:
            return

        routine_text = ' '.join(text)

        channel = self.get_channel(ctx.author.channel.name)

        logging.info(channel)

        @routines.routine(seconds=int(seconds), minutes=int(minutes), hours=int(hours), wait_first=False)
        async def temp_routine():
            await channel.send(routine_text)

        # Starts routine
        self.routines[ctx.author.channel.name + '_' + name] = temp_routine
        self.routines[ctx.author.channel.name + '_' + name].start()

        # Adds routine to db
        custom_commands.add_routine(
            ctx.author.channel.name,
            name,
            seconds,
            minutes,
            hours,
            routine_text
        )
        await ctx.send('Routine créée avec succès SeemsGood')


    @commands.command(name="routine_stop")
    async def routine_stop(self, ctx: commands.Context, name):
        if not ctx.author.is_mod:
            return

        # Stops routine
        logging.info(self.routines)
        self.routines[ctx.author.channel.name + '_' + name].cancel()
        logging.info(self.routines)

        custom_commands.remove_routine(ctx.author.channel.name, name)
        await ctx.send('Routine stoppée avec succès MrDestructoid')

    ## STREAM QUEUES ##
     
    @commands.command(name="startqueue")
    async def starting_queue(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
            
        channel = ctx.author.channel.name.lower()
        onoff = 1
        starting_queue = custom_commands.queue_on_off(channel, onoff)
        
        if starting_queue is not False:
            await ctx.send(f"La file est désormais ouverte, tapez !join pour y entrer MrDestructoid")
            
            
    @commands.command(name="stopqueue")
    async def stopping_queue(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
            
        channel = ctx.author.channel.name.lower()
        onoff = 0
        starting_queue = custom_commands.queue_on_off(channel, onoff)
        
        if starting_queue is not False:
            await ctx.send(f"La file est désormais fermée MrDestructoid")
        
        
        
    @commands.command(name="join")
    async def player_join_queue(self, ctx: commands.Context):
    
        active_queue = custom_commands.queue_active_check(ctx.author.channel.name)
        print(active_queue)
        if active_queue == False: #Ends the function is queue is not active
           return


        queue_player_join = custom_commands.join_queue(ctx.author.channel.name, ctx.author.name)
        
        if queue_player_join is True:
            await ctx.send(f"@{ctx.author.name} est entré dans la file MrDestructoid")

    @commands.command(name="leave") #leaving the queue
    async def player_leave_queue(self, ctx: commands.Context):


        queue_player_leave = custom_commands.leave_queue(ctx.author.channel.name, ctx.author.name)
        
        if queue_player_leave is True:
            await ctx.send(f"@{ctx.author.name} a quitté la file MrDestructoid")



    @commands.command(name="clearqueue") #command to clear the stream queue
    async def player_clear_queue(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return

        queue_player_clear = custom_commands.clear_queue(ctx.author.channel.name)
        
        if queue_player_clear is True:
            await ctx.send(f"La file a été évacuée, tout le monde dehors les margoulins MrDestructoid")
            


    @commands.command(name="kick")
    async def player_kick_queue(self, ctx: commands.Context, target):
        if not ctx.author.is_mod:
            return

        user = str(target.replace('@',''))
        queue_player_leave = custom_commands.leave_queue(ctx.author.channel.name, user)
        
        if queue_player_leave is True:
            await ctx.send(f"@{user} a été éjecté de la file. {user} pas sage MrDestructoid")


    @commands.command(name="next")
    async def player_next_queue(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
            
        channel = ctx.author.channel.name.lower()
        

        queue_player = custom_commands.queue_next(channel)
        
        if queue_player is not False:
            await ctx.send(f"C'est à ton tour @{queue_player} MrDestructoid")

            
        

    ## QUOTE AUTHORS ##

    @commands.command(name="author_add")
    async def author_add(self, ctx: commands.Context, *text):
        if not ctx.author.is_mod:
            return
            
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.add_author(channel, text)
        await ctx.send(f"Auteur/Source ajouté(e) avec succès MrDestructoid")


    @commands.command(name="author_del")
    async def author_del(self, ctx: commands.Context, *text):
        if not ctx.author.is_mod:
            return
            
        channel = ctx.author.channel.name.lower()
        text = ' '.join(text)

        custom_commands.del_author(channel, text)
        await ctx.send(f"Auteur/Source retiré(e) avec succès MrDestructoid")


    #Listing authors/sources for !citation command, not enabled yet
    @commands.command(name="author_list")
    async def author_list(self, ctx: commands.Context):
        channel = ctx.author.channel.name.lower()

        auteurs_raw = custom_commands.list_author(channel)
        auteurs = str(auteurs_raw)[1:-1]

        await ctx.send(f"Liste des auteurs/sources autorisés pour la commande !citation : {auteurs}")
        

    ## GENERAL FUNCTIONS ##
    @commands.command(name="git", aliases=['source'])
    async def git(self, ctx: commands.Context):
        await ctx.send(
            f'Tu veux voir mon code source ? Il est ici : https://github.com/LeDindonDeLaForce/LeDindoBOT MrDestructoid'
        )

    @commands.command(name="list")
    async def list(self, ctx: commands.Context):
        list = []
        for command in self.commands:
            list.append(command)

        list.sort()
        list = str(list)[1:-1] #remove list square brackets

        await ctx.send(f'La liste des commandes de ledindobot (hors custom) : {list}')




    @commands.command(name="join")
    async def join(self, ctx: commands.Context, channel):
        if ctx.author.name == os.environ['CHANNEL'] or ctx.author.name == channel:
            await ctx.send(f'Joining channel {channel}')

            await self.join_channels({channel})
            self.vip_so[channel] = {}
            add_channel(channel)

    @commands.command(name="leave")
    async def leave(self, ctx: commands.Context, channel):
        if ctx.author.name == os.environ['CHANNEL'] or ctx.author.name == channel:
            await ctx.send(f'Leaving channel {channel}')

            logging.info(f"PART #{channel}\r\n")
            await self._connection.send(f"PART #{channel}\r\n")
            leave_channel(channel)

    @commands.command(name="draw")
    async def draw(self, ctx: commands.Context):
        giveaway = list(self.giveaway)
        winners = random.sample(giveaway, k=5)
        games = ['SUPERHOT', 'Slay the spire',
                 'Tooth and Tail', 'Dear Esther', 'Max Payne 3']
        random.shuffle(games)
        for winner, game in zip(winners, games):
            await ctx.send(f'Félicitations {winner}! Tu as remporté {game}! SeemsGood')

    @commands.command(name="giveawayadd")
    async def giveawayadd(self, ctx: commands.Context, user: User = None):
        await ctx.send(f'{user.name} entered the giveaway!')
        self.giveaway.add(user.name)


if __name__ == "__main__":
    logging.basicConfig(
        encoding='utf-8',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler()
        ]
    )

bot = ledindobot()
#    bot.pubsub_client = client
bot.run()
