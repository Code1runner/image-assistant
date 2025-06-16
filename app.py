import io
import os

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from faq_utils import find_best_match, load_faq, prepare_faq_embeddings
from vision_utils import analyze_image, generate_description_and_tags

import openai
load_dotenv()  # Load environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

st.set_page_config(
    page_title="Asystent Opisywania Obrazu",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define images for user and assistant
user_avatar = "👤"  # Unicode character for a user icon
assistant_avatar = "🤖"  # Unicode character for a robot icon

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        background-color: #ffffff;
        color: #000000; /* Ensure text is black */
    }
    </style>
    """,

    unsafe_allow_html=True,
)


def main():
    """
    Main function to run the Streamlit app for image description and FAQ.
    """
    st.title("🧠 Asystent Opisywania Obrazu")
    st.markdown(
        "Wgraj zdjęcie, a my je przeanalizujemy i stworzymy opis oraz tagi."
    )

    faq = load_faq()
    faq = prepare_faq_embeddings(faq)  # Prepare embeddings for FAQ questions

    uploaded_file = st.file_uploader("📷 Wybierz obraz", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes))
        # Set a maximum width for the displayed image
        max_width = 400
        if image.width > max_width:
            image = image.resize((max_width, int(image.height * (max_width / image.width))))

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Podgląd obrazu")

        with col2, st.spinner("🔎 Analiza obrazu..."):
            vision_response = analyze_image(image_bytes)

            st.subheader("🔍 Rozpoznane etykiety:")
            st.write(", ".join(vision_response.labels))  # Display as comma-separated list
            st.subheader("📌 Rozpoznane obiekty:")
            st.write(", ".join(vision_response.objects))  # Display as comma-separated list

            result = generate_description_and_tags(
                vision_response.labels, vision_response.objects
            )
            st.subheader("📝 Opis i tagi (wygenerowane przez GPT):")
            st.markdown(result)

    # Initialize or retrieve chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header("💬 Pytania i odpowiedzi")

    # Display three buttons with FAQ questions
    if faq:  # Check if FAQ is not empty
        num_buttons = min(3, len(faq))  # Ensure we don't exceed the number of FAQ items
        for i in range(num_buttons):
            if st.button(faq[i].question):
                with st.spinner("Szukam odpowiedzi..."):
                    answer, score = find_best_match(faq[i].question, faq)
                    if answer:
                        st.session_state.chat_history.append(  # Removed score from display
                            {"question": faq[i].question, "answer": f" {answer}"}
                        )
                    else:
                        st.session_state.chat_history.append(
                            {"question": faq[i].question, "answer": "Nie znam odpowiedzi na to pytanie."}
                        )
    else:
        st.write("Brak pytań w FAQ.")

    # Allow users to type their own questions
    user_question = st.text_input("Lub wpisz własne pytanie:")
    if user_question and user_question != st.session_state.get("previous_question", ""):
        with st.spinner("Szukam odpowiedzi..."):
            answer, score = find_best_match(user_question, faq)
            if answer:
                st.session_state.chat_history.append(
                    {"question": user_question, "answer": f"Odpowiedź: {answer}"}  # Removed score from display
                )
            else:
                st.session_state.chat_history.append(
                    {"question": user_question, "answer": "Nie znam odpowiedzi na to pytanie."}
                )
        st.session_state.previous_question = user_question


    # Display chat history
    # Use a reversed list to show the most recent questions at the bottom
    for chat in reversed(st.session_state.chat_history):
        st.markdown(f"**Pytanie:** {chat['question']}")
        st.markdown(f"**Odpowiedź:** {chat['answer']}")


if __name__ == "__main__":
    main()