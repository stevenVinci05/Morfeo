import re
from transformers import pipeline
from deep_translator import GoogleTranslator

classifier = pipeline("text-classification", model="unitary/toxic-bert")

ETICHETTE_TOSSICHE = {
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate"
}

def preprocess_text(text):
    text = text.lower()
    substitutions = {
        '4': 'a',
        '3': 'e',
        '1': 'i',
        '0': 'o',
        '@': 'a',
        '$': 's',
        '+': 't',
        '7': 't',
        '5': 's',
        '8': 'b',
    }
    for k, v in substitutions.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def is_tossic(testo, soglia=0.2):
    testo_pulito = preprocess_text(testo)
    
    try:
        testo_tradotto = GoogleTranslator(source='auto', target='en').translate(testo_pulito)
    except Exception as e:
        print(f"❌ Errore nella traduzione: {e}")
        return False

    risultati = classifier(testo_tradotto)
    for r in risultati:
        if r["label"].lower() in ETICHETTE_TOSSICHE and r["score"] >= soglia:
            print(f"❌ Tossico: '{testo}' → {r['label']} = {r['score']:.2f}")
            return True
    return False
