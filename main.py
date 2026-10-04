import os
import sys
from dotenv import load_dotenv
from rodiumai import RodiumAI

# Charger la clé API
load_dotenv()
api_key = os.getenv("RODIUMAI_API_KEY")

if not api_key:
    print("Erreur : La clé API RODIUMAI_API_KEY est introuvable dans le fichier .env.")
    sys.exit(1)

# Initialiser le client RodiumAI avec le SDK
client = RodiumAI(api_key=api_key)

def step_chat():
    while True:
        print("\n" + "="*10 + " [Python] Étape 1: Chat " + "="*10)
        question = input("Votre question : ").strip()
        if not question:
            continue

        try:
            response = client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[{"role": "user", "content": question}]
            )
            content = response.choices[0].message.content
            cost = getattr(response, 'cost_rodi', 'N/A')
            
            print(f"\n[Réponse] :\n{content}")
            print(f"Coût : {cost} RODI")
        except Exception as e:
            print(f"Erreur : {e}")

        choice = input("\nRester sur cette étape (r) ou passer à la suivante (s) ? [r/s] : ").strip().lower()
        if choice == 's':
            return 'next'

def step_image():
    while True:
        print("\n" + "="*10 + " [Python] Étape 2: Image " + "="*10)
        prompt = input("Décrivez l'image : ").strip()
        if not prompt:
            continue

        try:
            print("Génération de l'image en cours...")
            response = client.images.generate(
                model="stabilityai/stable-diffusion-3",
                prompt=prompt,
                response_format="b64_json"
            )
            # Enregistrement de l'image
            import base64
            image_bytes = base64.b64decode(response.data[0].b64_json)
            with open("image.png", "wb") as f:
                f.write(image_bytes)
            print("Image enregistrée : image.png")
        except Exception as e:
            print(f"Erreur : {e}")

        choice = input("\nRevenir en arrière (b), rester (r) ou passer à la suivante (s) ? [b/r/s] : ").strip().lower()
        if choice == 'b':
            return 'back'
        elif choice == 's':
            return 'next'

def step_video():
    while True:
        print("\n" + "="*10 + " [Python] Étape 3: Vidéo " + "="*10)
        prompt = input("Décrivez la vidéo : ").strip()
        if not prompt:
            continue

        try:
            print("Génération de la vidéo en cours (patientez)...")
            response = client.videos.generate(
                model="openai/sora",
                prompt=prompt
            )
            # Téléchargement et enregistrement de la vidéo
            import requests
            video_url = response.data[0].url
            vid_data = requests.get(video_url).content
            with open("video.mp4", "wb") as f:
                f.write(vid_data)
            print("Vidéo enregistrée : video.mp4")
        except Exception as e:
            print(f"Erreur : {e}")

        choice = input("\nRevenir en arrière (b), rester (r) ou quitter (q) ? [b/r/q] : ").strip().lower()
        if choice == 'b':
            return 'back'
        elif choice == 'q':
            break

def main():
    step = 1
    while step <= 3:
        if step == 1:
            if step_chat() == 'next':
                step = 2
        elif step == 2:
            res = step_image()
            if res == 'back':
                step = 1
            elif res == 'next':
                step = 3
        elif step == 3:
            res = step_video()
            if res == 'back':
                step = 2
            else:
                break

if __name__ == "__main__":
    main()