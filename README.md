# Veritas AI - Content Integrity Suite 🛡️

Veritas AI is a corporate-grade content suite designed to humanize AI-generated text and verify content authenticity using real-time search engine verification. Built with a premium, sleek glassmorphism dark theme, the application provides two independent content engines with unlimited word count support.

---

## Key Features

### 📝 AI Content Humanizer
* **Perplexity & Burstiness Optimization**: Rewrites text by varying sentence structures and replacing predictable AI signatures (such as *"delve"*, *"moreover"*, *"testament"*, etc.).
* **Custom Phrasing and Flow**: Restructures paragraphs to emulate high-quality human writing while preserving the original meaning and core arguments.
* **Tone Adjustments**: Choose between Natural, Casual, Professional, Academic, or Creative tones.
* **Intensity Sliders**: Light, Medium, or High rewrite strengths.

### 🔍 Plagiarism Checker
* **Google Search Grounding**: Integrates Google Search to scan the internet for duplicate content and paraphrasing.
* **Aggregated Similarity Score**: Displays an overall plagiarism percentage with color-coded safety indicators (Safe, Caution, High Risk).
* **Clickable Sources**: Returns a list of matched web pages with URLs, titles, and match confidence scores.
* **Sentence-Level Highlighting**: Color-codes matched sentences to pinpoint exactly which sections require editing.

### 📄 Advanced PDF Handler
* **Logical Text Extraction**: Parse uploaded PDF documents page-by-page.
* **Doc Reconstruction**: Aggregates extracted pages into logical chunks to handle documents of any length.
* **Formatted PDF Exports**: Export your humanized content as a styled, clean PDF or plain text file.

---

## Tech Stack
* **Frontend UI**: [Streamlit](https://streamlit.io/) (with custom CSS glassmorphic overrides)
* **AI Core**: [Google GenAI SDK](https://github.com/google/generative-ai-python) (using Gemini models)
* **Real-time Search**: Google Search Grounding Tool
* **PDF Core**: `pypdf` (extraction) and `fpdf2` (generation)

---

## Local Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Bobby262001/veritas-ai.git
   cd veritas-ai
   ```

2. **Create a virtual environment & install dependencies**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On macOS/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure your API Key**:
   Create a `.env` file in the root folder:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

---

## Cloud Deployment (Streamlit Cloud)

Veritas AI is optimized for cloud deployment. To host it:

1. **Deploy from GitHub**: Link your repository to [Streamlit Community Cloud](https://share.streamlit.io/).
2. **Secure Secrets Configuration**: Do **not** upload your `.env` file to GitHub. Instead, configure it securely in the Streamlit Cloud dashboard:
   - Open your deployed app settings.
   - Go to the **Secrets** tab.
   - Paste your key:
     ```toml
     GEMINI_API_KEY = "your_gemini_api_key_here"
     ```
   - Save the changes to launch the application live.

---

## Security and Privacy
* The application loads the API key securely from the environment using Streamlit secrets and `.env` files.
* Text inputs and PDF uploads are parsed locally and transmitted securely to Google's API endpoints. Files are never stored permanently on third-party servers.
