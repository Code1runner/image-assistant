# 📜 Image Assistant

Image Assistant is a lightweight web app built with Streamlit that allows users to:

* Analyze images using Google Vision API
* Generate captions and tags
* Answer image-related questions using OpenAI's GPT models

---

## 🚀 Features

* Upload and analyze images
* Automatically tag images
* Ask image-related questions
* Simple, user-friendly interface
* Built with Streamlit and Docker

---

## 🧰 Tech Stack

* Python 3.12
* Streamlit
* Google Cloud Vision API
* OpenAI GPT-4
* Docker

---

## 🥪 Run Locally with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/michalgabb98/image-assistant.git
cd image-assistant/image_assistant
```

### 2. Set Up Environment Variables

Create a `.env` file based on the `.env_example` file:

```bash
cp .env_example .env
```

Edit `.env` and provide your API keys:

```env
GOOGLE_VISION_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
```

### 3. Build and Run the Docker Container

```bash
docker build -t streamlit-app .
docker run -p 8080:8080 streamlit-app
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

---

## 📝 Environment Variables

| Variable                | Description                |
| ----------------------- | -------------------------- |
| `GOOGLE_VISION_API_KEY` | Your Google Vision API key |
| `OPENAI_API_KEY`        | Your OpenAI API key        |

---

## 📁 File Structure

```
.
├── app.py              # Main Streamlit app
├── Dockerfile          # Docker config
├── requirements.txt    # Python dependencies
├── .env_example        # Sample environment file
├── vision_utils.py     # Google Vision API logic
├── models.py           # GPT-4 communication logic
├── faq_utils.py        # FAQ chatbot utilities
├── faq.json            # Sample FAQ data
```

---

## 📦 Deployment

This app can be deployed on [Google Cloud Run](https://cloud.google.com/run) using a Docker container.

---

## 🧑‍💻 Author

Made by [Code1Runner](https://github.com/michalgabb98)

---

## �� License

MIT License
