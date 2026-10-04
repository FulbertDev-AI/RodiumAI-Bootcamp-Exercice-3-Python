import os
import sys
import asyncio
import base64
import requests
from dotenv import load_dotenv
from rodiumai import RodiumAI

# Charger la clé API
load_dotenv()
api_key = os.getenv("RODIUMAI_API_KEY")

if not api_key:
    print("Erreur : La clé API RODIUMAI_API_KEY est introuvable dans le fichier .env.")
    sys.exit(1)

# Initialiser le client RodiumAI
client = RodiumAI(api_key=api_key)

# Fonction utilitaire pour lire les inputs utilisateur de manière asynchrone
async def input_async(prompt_text):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, input, prompt_text)

async def step_chat():
    while True:
        print("\n" + "="*10 + " [Python SDK] Étape 1: Chat " + "="*10)
        question = (await input_async("Votre question : ")).strip()
        if not question:
            continue

        try:
            # Utilisation de la syntaxe officielle de la documentation
            response = await client.chat(question)
            
            # Extraction du contenu de la réponse
            content = response.choices[0].message.content
            cost = getattr(response, 'cost_rodi', 'N/A')
            
            print(f"\n[Réponse] :\n{content}")
            print(f"Coût : {cost} RODI")
        except Exception as e:
            print(f"Erreur : {e}")

        choice = (await input_async("\nRester sur cette étape (r) ou passer à la suivante (s) ? [r/s] : ")).strip().lower()
        if choice == 's':
            return 'next'

async def step_image():
    while True:
        print("\n" + "="*10 + " [Python SDK] Étape 2: Image " + "="*10)
        prompt = (await input_async("Décrivez l'image : ")).strip()
        if not prompt:
            continue

        try:
            print("Génération de l'image en cours...")
            response = await client.images.generate(
                model="google/gemini-3.1-flash-lite-image",
                prompt=prompt,
                response_format="b64_json"
            )
            image_bytes = base64.b64decode(response.data[0].b64_json)
            with open("image.png", "wb") as f:
                f.write(image_bytes)
            print("Image enregistrée : image.png")
        except Exception as e:
            print(f"Erreur : {e}")

        choice = (await input_async("\nRevenir en arrière (b), rester (r) ou passer à la suivante (s) ? [b/r/s] : ")).strip().lower()
        if choice == 'b':
            return 'back'
        elif choice == 's':
            return 'next'
async def step_video():
    while True:
        print("\n" + "="*10 + " [Python SDK] Étape 3: Vidéo " + "="*10)
        prompt = (await input_async("Décrivez ce que vous voulez générer/analyser : ")).strip()
        if not prompt:
            continue

        try:
            print("Traitement en cours avec le modèle Gemini...")
            # Utilisation de client.chat avec le modèle vidéo/multimodal spécifié
            response = await client.chat(
                messages=[{"role": "user", "content": prompt}],
                model="google/veo-3.1-fast"
            )
            
            # Récupération de la réponse textuelle du modèle
            content = response.choices[0].message.content
            cost = getattr(response, 'cost_rodi', 'N/A')
            
            print(f"\n[Réponse] :\n{content}")
            print(f"Coût : {cost} RODI")
            
        except Exception as e:
            print(f"Erreur : {e}")

        choice = (await input_async("\nRevenir en arrière (b), rester (r) ou quitter (q) ? [b/r/q] : ")).strip().lower()
        if choice == 'b':
            return 'back'
        elif choice == 'q':
            break

async def main():
    step = 1
    while step <= 3:
        if step == 1:
            if await step_chat() == 'next':
                step = 2
        elif step == 2:
            res = await step_image()
            if res == 'back':
                step = 1
            elif res == 'next':
                step = 3
        elif step == 3:
            res = await step_video()
            if res == 'back':
                step = 2
            else:
                break

if __name__ == "__main__":
    asyncio.run(main())