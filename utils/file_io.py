import json
import os

def ReadFile(filePath):
    if not os.path.exists(filePath):
        return []
    with open(filePath, "r", encoding="utf-8") as f:
        return json.load(f)
    
def WriteFile(filePath, lista):
    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)