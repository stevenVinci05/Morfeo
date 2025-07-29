# Morfeo Bot Discord

Bot Discord con funzionalità di moderazione, filtri anti-spam e analisi della tossicità.

## Configurazione

### 1. Installazione Dipendenze
```bash
pip install -r requirements.txt
```

### 2. Configurazione Token Discord

**Opzione A: File .env (Raccomandato)**
1. Crea un file `.env` nella root del progetto
2. Aggiungi il tuo token Discord:
```
DISCORD_TOKEN=il_tuo_token_qui
```

**Opzione B: Variabile Ambiente**
- **Windows (PowerShell):**
  ```powershell
  $env:DISCORD_TOKEN="il_tuo_token_qui"
  ```
- **Windows (CMD):**
  ```cmd
  set DISCORD_TOKEN=il_tuo_token_qui
  ```
- **Linux/Mac:**
  ```bash
  export DISCORD_TOKEN=il_tuo_token_qui
  ```

### 3. Avvio Bot
```bash
python bot.py
```

## Funzionalità

### Comandi Disponibili
Tutti i comandi funzionano sia come **prefix commands** (`!comando`) che come **slash commands** (`/comando`):

#### Utility
- `/ciao` - Saluta l'utente

#### Admin
- `/delete [numero]` - Cancella messaggi
- `/clear_user @utente [numero]` - Cancella messaggi di un utente
- `/ban @utente [motivo]` - Banna un utente
- `/kick @utente [motivo]` - Espelle un utente
- `/mute @utente [motivo]` - Muta un utente
- `/list_bans` - Mostra lista utenti bannati
- `/unban utente` - Sbanna un utente
- `/add parola` - Aggiunge parola alla lista ban
- `/rem parola` - Rimuove parola dalla lista ban
- `/provaI parola` - Testa tossicità di una parola

### Funzionalità Automatiche
- **Anti-spam**: Rileva e gestisce messaggi spam
- **Filtro parole vietate**: Rimuove messaggi con parole inappropriate
- **Analisi tossicità IA**: Usa AI per rilevare contenuti offensivi

## Sicurezza
- Il token Discord è gestito tramite variabili ambiente
- Nessuna informazione sensibile è hardcoded nel codice
- Il file `.env` dovrebbe essere aggiunto a `.gitignore` 