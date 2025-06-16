import json
import numpy as np
import openai
from typing import List, Tuple, Optional
from sklearn.metrics.pairwise import cosine_similarity  # Ensure scikit-learn is installed
from models import FAQItem


def load_faq(filename: str = "faq.json") -> List[FAQItem]:
    """
    Loads FAQ data from a JSON file.

    Args:
        filename (str): The name of the JSON file containing the FAQ data.

    Returns:
        List[FAQItem]: A list of FAQItem objects.
    """
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [FAQItem(**item) for item in data]


def get_embedding(text: str) -> np.ndarray:
    """
    Generates an embedding for a given text using OpenAI's embedding model.

    Args:
        text (str): The text to embed.

    Returns:
        np.ndarray: The embedding vector as a NumPy array.
    """
    try:
        response = openai.embeddings.create(
            model="text-embedding-3-small", input=text
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
        print(f"[ERROR] Failed to generate embedding for text: '{text}'. Error: {e}")
        return np.array([])  # Or handle the error in a way that suits your application


def prepare_faq_embeddings(faq: List[FAQItem]) -> List[FAQItem]:
    """
    Prepares embeddings for all questions in the FAQ.

    Args:
        faq (List[FAQItem]): A list of FAQItem objects.

    Returns:
        List[FAQItem]: The FAQ list with embeddings added to each item.
    """
    for item in faq:
        item.embedding = get_embedding(item.question).tolist()
    return faq


def find_best_match(
    user_question: str, faq: List[FAQItem], threshold: float = 0.85
) -> Tuple[Optional[str], float]:
    """
    Finds the best matching question in the FAQ for a given user question.

    Args:
        user_question (str): The user's question.
        faq (List[FAQItem]): The FAQ list with embeddings.
        threshold (float): The similarity threshold for a match.

    Returns:
        Tuple[Optional[str], float]: The answer to the best matching question and the similarity score, or (None, best_score) if no match is found.
    """
    user_embedding = get_embedding(user_question)
    similarities = cosine_similarity(
        [user_embedding], [np.array(item.embedding) for item in faq]
    )[0]
    best_match_index = np.argmax(similarities)
    best_score = similarities[best_match_index]

    if best_score >= threshold:
        return faq[best_match_index].answer, best_score
    else:
        return None, best_score