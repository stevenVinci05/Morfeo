# 🔧 Sincronizzazione Manuale Comandi

## Il Problema
I comandi `hybrid_command` non vengono automaticamente sincronizzati con Discord. Il bot ha tutti i permessi necessari, ma i comandi non appaiono come slash commands.

## 🛠️ Soluzioni

### 1. **Avvia il Bot**
```bash
py bot.py
```

### 2. **Usa il Comando `/sync`**
Una volta che il bot è online, vai nel tuo server Discord e digita:
```
/sync
```

Questo comando:
- ✅ Registra manualmente tutti i comandi hybrid nell'albero slash
- ✅ Sincronizza i comandi con Discord
- ✅ Mostra il numero di comandi sincronizzati

### 3. **Verifica lo Stato**
Usa il comando:
```
/comandi_status
```

Questo ti mostrerà:
- 📊 Numero di comandi hybrid definiti
- 🌳 Numero di comandi nell'albero
- 🔑 Se il bot ha i permessi necessari

### 4. **Comandi Disponibili**

#### Comandi di Sincronizzazione:
- `/sync` - Sincronizza per questo server
- `/sync_global` - Sincronizza globalmente (solo proprietario)
- `/comandi_status` - Mostra stato comandi

#### Comandi Utilità:
- `/ciao` - Saluta l'utente
- `/ping` - Mostra latenza bot
- `/comandi` - Lista comandi disponibili

#### Comandi Amministrativi:
- `/delete [numero]` - Cancella messaggi
- `/ban @utente [motivo]` - Banna utente
- `/kick @utente [motivo]` - Espelle utente
- `/mute @utente [motivo]` - Muta utente
- E molti altri...

## 🔍 Debug

Se i comandi ancora non funzionano:

1. **Verifica Permessi Bot**:
   - Il bot deve avere il permesso "Use Slash Commands"
   - Il bot deve essere amministratore o avere permessi elevati

2. **Aspetta qualche minuto**:
   - Discord può impiegare tempo per aggiornare i comandi
   - Prova a riavviare Discord

3. **Controlla i Log**:
   - Il bot mostra informazioni dettagliate durante l'avvio
   - Cerca errori nella console

## 📝 Note Importanti

- I comandi funzionano sia come slash (`/comando`) che con prefisso (`!comando`)
- La sincronizzazione avviene automaticamente all'avvio
- Usa `/sync` per forzare la sincronizzazione manuale
- I nuovi comandi vengono sincronizzati quando aggiungi il comando `/sync`

## 🚀 Prossimi Passi

1. Avvia il bot
2. Usa `/sync` nel server
3. Aspetta 1-2 minuti
4. Prova i comandi slash!

Se ancora non funziona, controlla i log del bot per errori specifici. 