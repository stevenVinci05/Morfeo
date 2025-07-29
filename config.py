import os

# Controlla se il file .env esiste
if not os.path.exists('.env'):
    print("⚠️  File .env non trovato!")
    print("📝 Crea un file .env nella root del progetto con:")
    print("   DISCORD_TOKEN=il_tuo_token_qui")

TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    print("❌ ERRORE: La variabile ambiente DISCORD_TOKEN non è impostata!")
    print("💡 Soluzioni:")
    print("   1. Crea un file .env con DISCORD_TOKEN=il_tuo_token_qui")
    print("   2. Imposta la variabile ambiente DISCORD_TOKEN nel sistema")
    print("   3. Esegui: set DISCORD_TOKEN=il_tuo_token_qui (Windows)")
    print("   4. Esegui: export DISCORD_TOKEN=il_tuo_token_qui (Linux/Mac)")
    raise ValueError('La variabile ambiente DISCORD_TOKEN non è impostata!')

print("✅ Token Discord caricato correttamente dalle variabili ambiente")

PREFIX = '!'
MAX_MSG = 3
MAX_TMP = 5
JSON_BANNED = 'data/banned_words.json'
