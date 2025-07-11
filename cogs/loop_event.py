import discord
from discord.ext import commands
import config
import time
from utils.file_io import ReadFile
from collections import defaultdict, deque
from utils.toxicity_filter import is_tossic  # IA per analisi tossicità

class LoopEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_log = defaultdict(lambda: deque())
        self.bannedWords = ReadFile(config.JSON_BANNED)
        print("✅ LoopEvents caricato correttamente")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        print(f"📩 Messaggio ricevuto da {message.author.name}: {message.content}")

        now = time.time()
        user_id = message.author.id
        channel_id = message.channel.id

        self.message_log[user_id].append((now, message.id, channel_id))
        while self.message_log[user_id] and now - self.message_log[user_id][0][0] > config.MAX_TMP:
            self.message_log[user_id].popleft()

        print(f"📊 {message.author.name}: {len(self.message_log[user_id])} messaggi recenti")

        if len(self.message_log[user_id]) > config.MAX_MSG:
            print(f"⚠️ SPAM rilevato da {message.author.name}")

            from collections import defaultdict
            msg_per_channel = defaultdict(list)
            for _, msg_id, ch_id in list(self.message_log[user_id]):
                msg_per_channel[ch_id].append(msg_id)

            for ch_id, msg_ids in msg_per_channel.items():
                channel = self.bot.get_channel(ch_id)
                if channel:
                    try:
                        def check(m):
                            return m.id in msg_ids and m.author.id == user_id
                        deleted = await channel.purge(limit=100, check=check, bulk=True)
                        print(f"🧹 Eliminati {len(deleted)} messaggi da {channel.name}")
                    except discord.Forbidden:
                        print(f"🚫 Permessi insufficienti per eliminare messaggi in {channel.name}")
                    except Exception as e:
                        print(f"❌ Errore in purge su {channel.name}: {e}")

            self.message_log[user_id].clear()

            try:
                await message.author.send(
                    "⚠️ Attenzione! Stai inviando troppi messaggi in poco tempo. Se continui, potresti essere bannato."
                )
            except discord.Forbidden:
                print(f"🚫 Impossibile inviare DM a {message.author.name} (DM chiusi)")
            except Exception as e:
                print(f"❌ Errore inviando DM a {message.author.name}: {e}")

            return  # interrompi ulteriore processing per questo messaggio

        contenuto = message.content.lower()

        #if message.author.guild_permissions.administrator:
        #    await self.bot.process_commands(message)
        #    return

        # Filtro parole vietate
        if any(parola in contenuto for parola in self.bannedWords):
            try:
                await message.delete()
                await message.channel.send(
                    f"🚫 {message.author.mention}, il tuo messaggio conteneva una parola vietata.",
                    delete_after=5
                )
            except Exception as e:
                print(f"Errore eliminando messaggio: {e}")
            return

        # Filtro IA tossicità
        try:
            if is_tossic(message.content):
                await message.delete()
                await message.channel.send(
                    f"🧠 {message.author.mention}, il tuo messaggio è stato considerato offensivo e rimosso.",
                    delete_after=5
                )
                try:
                    await message.author.send(
                        "⚠️ Il tuo messaggio è stato rimosso perché ritenuto offensivo. Se pensi sia un errore, contatta un moderatore."
                    )
                except discord.Forbidden:
                    pass
                return
        except Exception as e:
            print(f"❌ Errore durante analisi IA: {e}")

        await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(LoopEvents(bot))
