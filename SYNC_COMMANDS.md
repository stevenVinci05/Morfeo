# Sincronizzazione Comandi Discord Bot

## Come Funziona

Il bot **Morfeo** sincronizza automaticamente i comandi slash ogni volta che viene avviato. Ecco come funziona:

### 🔄 Sincronizzazione Automatica

1. **All'avvio del bot**: Quando il bot si connette, l'evento `on_ready()` viene attivato
2. **Per ogni server**: Il bot sincronizza i comandi slash con tutti i server a cui è connesso
3. **Nuovi server**: Quando il bot viene aggiunto a un nuovo server, i comandi vengono sincronizzati automaticamente

### 📋 Comandi Disponibili

#### Comandi Slash (/) e Prefisso (!)
- `/ciao` - Saluta l'utente
- `/ping` - Mostra la latenza del bot
- `/comandi` - Mostra tutti i comandi disponibili

#### Comandi Amministrativi
- `/delete [numero]` - Cancella messaggi
- `/clear_user @utente [numero]` - Cancella messaggi di un utente
- `/ban @utente [motivo]` - Banna un utente
- `/kick @utente [motivo]` - Espelle un utente
- `/mute @utente [motivo]` - Muta un utente
- `/unban @utente` - Sbanna un utente
- `/list_bans` - Mostra lista utenti bannati
- `/add [parola]` - Aggiunge parola alla lista ban
- `/rem [parola]` - Rimuove parola dalla lista ban
- `/provai [parola]` - Testa tossicità di una parola
- `/info-user @utente` - Informazioni su un utente
- `/sync` - Sincronizza comandi per questo server
- `/sync_global` - Sincronizza comandi globalmente (solo proprietario)

### 🛠️ Comandi di Sincronizzazione

#### `/sync`
- **Permessi**: Amministratore
- **Funzione**: Sincronizza i comandi slash per il server corrente
- **Uso**: Utile quando si aggiungono nuovi comandi o si modificano quelli esistenti

#### `/sync_global`
- **Permessi**: Proprietario del bot
- **Funzione**: Sincronizza i comandi slash globalmente
- **Nota**: Può richiedere fino a 1 ora per propagarsi su tutti i server

### 📊 Output del Bot

Quando il bot si avvia, vedrai output simili a questo:

```
✅ Morfeo#1234 è online!
🆔 Bot ID: 123456789012345678
📊 Connesso a 3 server
🔄 Iniziando sincronizzazione comandi slash...
✅ Server 'Il Mio Server' (123456789012345678): 15 comandi sincronizzati
✅ Server 'Altro Server' (987654321098765432): 15 comandi sincronizzati
🎯 Sincronizzazione completata:
   📋 Server processati: 2/2
   🔧 Comandi totali sincronizzati: 30

📝 Comandi disponibili:
   /ciao - Saluta l'utente.
   /ping - Mostra la latenza del bot.
   /comandi - Mostra i comandi disponibili del bot.
   /delete - Cancella un numero di messaggi.
   ...
```

### 🔧 Risoluzione Problemi

#### I comandi slash non appaiono
1. Verifica che il bot abbia il permesso "Use Slash Commands"
2. Usa `/sync` per forzare la sincronizzazione
3. Aspetta qualche minuto (Discord può impiegare tempo per aggiornare)

#### Errore di sincronizzazione
- Controlla i log del bot per errori specifici
- Verifica che tutti i cog siano caricati correttamente
- Assicurati che i comandi siano definiti correttamente

### 📝 Note Importanti

- I comandi sono definiti come `hybrid_command`, quindi funzionano sia come slash che con prefisso
- La sincronizzazione avviene automaticamente all'avvio
- I nuovi comandi vengono sincronizzati quando il bot si riavvia
- Per modifiche immediate, usa `/sync` o `/sync_global` 