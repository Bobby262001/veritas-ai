# Deploying Veritas AI to the Cloud (Free & Secure)

To share this application with someone in the UAE (or anywhere else in the world), you need to host it on the web. The easiest, fastest, and most official way to do this is using **Streamlit Community Cloud**, which is 100% free.

Follow these 4 simple steps to deploy your app in under 3 minutes:

---

### Step 1: Create a GitHub Repository
1. Go to [GitHub](https://github.com/) and log in (or sign up for a free account).
2. Create a new **Private** or **Public** repository (e.g., named `veritas-ai`).
3. Push the files in your project directory (`C:\Users\bhara\.gemini\antigravity\scratch\ai-content-tool`) to this repository:
   - Make sure `app.py`, `requirements.txt`, `core/`, and `utils/` are pushed.
   - **DO NOT** push the `.env` file containing your actual API key (keep your key secret and secure!).

---

### Step 2: Set Up Streamlit Community Cloud
1. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Click **Connect with GitHub** and log in.
3. Click the **New app** button.

---

### Step 3: Deploy the App
1. Fill in the deployment details:
   - **Repository**: Choose your newly created GitHub repository (e.g. `yourusername/veritas-ai`).
   - **Branch**: Select `main` or `master`.
   - **Main file path**: Type `app.py`.
2. Click **Deploy!** 
3. The platform will build your app and spin it up in about a minute. You will see a live URL (e.g., `https://veritas-ai.streamlit.app/`).

---

### Step 4: Add Your Gemini API Key Securely
Since you didn't upload your `.env` file to GitHub for security, you need to add your API key to Streamlit's settings:
1. In the bottom-right corner of your running Streamlit Cloud app dashboard, click **Manage App**.
2. Click on the **vertical ellipsis (three dots)** and select **Settings**.
3. Go to the **Secrets** tab.
4. Paste your Gemini API key inside the box exactly like this:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Save**. The app will automatically restart and pick up the key securely!

---

### 🎉 Sharing
Your app is now live! Simply copy the URL (e.g., `https://your-app-name.streamlit.app/`) and send it to your contact in the UAE. They will be able to upload PDFs or paste text and run plagiarism/humanizing scans instantly.
