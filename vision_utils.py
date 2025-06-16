import base64
import json
import os
from typing import List, Tuple

import requests
from dotenv import load_dotenv
import openai
from models import VisionResponse

load_dotenv()


def analyze_image(image_file: bytes) -> VisionResponse:
    """
    Analyzes an image using Google Cloud Vision API to detect labels and objects.

    Args:
        image_file (bytes): The image file as bytes.

    Returns:
        VisionResponse: An object containing lists of detected labels and objects.
    """
    if not image_file:
        print("Brak pliku obrazu.")
        return VisionResponse(labels=[], objects=[])

    try:
        content = base64.b64encode(image_file).decode("utf-8")
    except Exception as e:
        print(f"[ERROR] Błąd kodowania base64: {e}")
        return VisionResponse(labels=[], objects=[])

    vision_url = f"https://vision.googleapis.com/v1/images:annotate?key={os.getenv('GOOGLE_VISION_API_KEY')}"
    vision_payload = {
        "requests": [
            {
                "image": {"content": content},
                "features": [
                    {"type": "LABEL_DETECTION"},
                    {"type": "OBJECT_LOCALIZATION"},
                ],
            }
        ]
    }

    try:
        response = requests.post(vision_url, json=vision_payload)
        result = response.json()
    except Exception as e:
        print(f"[ERROR] Błąd przy wysyłaniu zapytania: {e}")
        return VisionResponse(labels=[], objects=[])

    try:
        labels = [
            ann["description"]
            for ann in result["responses"][0].get("labelAnnotations", [])
        ]
        objects = [
            obj["name"]
            for obj in result["responses"][0].get(
                "localizedObjectAnnotations", []
            )
        ]
        return VisionResponse(labels=labels, objects=objects)
    except Exception as e:
        print(f"[ERROR] Błąd parsowania odpowiedzi: {e}")
        return VisionResponse(labels=[], objects=[])


def generate_description_and_tags(labels: List[str], objects: List[str]) -> str:
    """
    Generates a description and tags for an image based on detected labels and objects using OpenAI's GPT-4 model.

    Args:
        labels (List[str]): List of labels detected in the image.
        objects (List[str]): List of objects detected in the image.

    Returns:
        str: A string containing a short description and a list of tags.
    """
    combined_info = labels + objects
    prompt = (
        "Na podstawie poniższych etykiet i obiektów z obrazu:\n"
        f"{', '.join(combined_info)}\n"
        "Wygeneruj krótki opis (1-2 zdania) oraz listę tagów (max 5):"
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] Błąd podczas generowania opisu: {e}")
        return "Nie udało się wygenerować opisu."