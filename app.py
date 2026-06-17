import streamlit as st
import os
import sys
from dotenv import load_dotenv

# Add project root directory to sys.path for cloud deployments
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load local environment variables if present
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Veritas AI - Content Integrity Suite",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injected Corporate Stylesheet with Animated Mesh Background and Glassmorphism
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    /* Overall font settings */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }
    
    /* Animated Gradient Background */
    .stApp {
        background: radial-gradient(circle at 10% 20%, rgba(15, 23, 42, 1) 0%, rgba(10, 15, 30, 1) 90%) !important;
        background-attachment: fixed !important;
    }
    
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: 
            radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.06) 0%, transparent 40%),
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.06) 0%, transparent 40%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 28px;
        margin-bottom: 24px;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        z-index: 1;
    }
    
    .glass-card:hover {
        border-color: rgba(59, 130, 246, 0.25);
        box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.07);
        transform: translateY(-2px);
    }
    
    /* Main title headers */
    .brand-title {
        font-weight: 800;
        background: linear-gradient(135deg, #F3F4F6 0%, #9CA3AF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 6px;
    }
    
    /* Custom buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.2) !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #1D4ED8 0%, #1E40AF 100%) !important;
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Text Input Overrides */
    .stTextArea textarea {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #F3F4F6 !important;
        border-radius: 8px !important;
        font-size: 14px !important;
    }
    .stTextArea textarea:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }
    
    /* Comparison windows */
    .compare-column {
        height: 480px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        line-height: 1.7;
        color: #E5E7EB;
        font-size: 14.5px;
    }
    
    /* Highlighted segments */
    .plagiarized-text {
        background-color: rgba(239, 68, 68, 0.12);
        border-bottom: 2px dashed #EF4444;
        color: #FCA5A5;
        padding: 1px 3px;
        border-radius: 2px;
        cursor: pointer;
        display: inline;
    }
    .original-text {
        color: #E5E7EB;
        display: inline;
    }
    
    /* Meter container */
    .meter-container {
        width: 100%;
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        overflow: hidden;
        height: 14px;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.04);
    }
    .meter-fill {
        height: 100%;
        border-radius: 20px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Source list item */
    .source-card {
        background: rgba(30, 41, 59, 0.4);
        border-left: 4px solid #3B82F6;
        border-right: 1px solid rgba(255, 255, 255, 0.03);
        border-top: 1px solid rgba(255, 255, 255, 0.03);
        border-bottom: 1px solid rgba(255, 255, 255, 0.03);
        padding: 16px;
        margin-bottom: 12px;
        border-radius: 0 10px 10px 0;
    }
    .source-card.danger {
        border-left-color: #EF4444;
    }
    .source-card.warning {
        border-left-color: #F59E0B;
    }
    
    /* Hide Streamlit components for official aesthetic */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Enterprise Header Navigation
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 24px; background: rgba(17, 24, 39, 0.6); border-radius: 12px; border: 1px solid rgba(255,255,255,0.04); backdrop-filter: blur(20px); margin-bottom: 28px;">
    <div style="display: flex; align-items: center; gap: 12px;">
        <span style="font-size: 22px; font-weight: 800; letter-spacing: 0.5px; background: linear-gradient(90deg, #60A5FA, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">VERITAS AI</span>
        <span style="background: rgba(59, 130, 246, 0.08); color: #60A5FA; font-size: 11px; font-weight: 600; padding: 2px 8px; border-radius: 20px; border: 1px solid rgba(59, 130, 246, 0.15);">ENTERPRISE EDITION</span>
    </div>
    <div style="display: flex; align-items: center; gap: 18px; color: #9CA3AF; font-size: 13.5px; font-weight: 500;">
        <span>Documentation</span>
        <span style="color: rgba(255,255,255,0.15);">|</span>
        <span>Developer API</span>
        <span style="color: rgba(255,255,255,0.15);">|</span>
        <span style="color: #34D399; display: flex; align-items: center; gap: 5px;">
            <span style="display: inline-block; width: 8px; height: 8px; background-color: #34D399; border-radius: 50%; animation: pulse 2s infinite;"></span>
            Security Certified
        </span>
    </div>
</div>
<style>
@keyframes pulse {
    0% { transform: scale(0.9); opacity: 1; }
    50% { transform: scale(1.2); opacity: 0.5; }
    100% { transform: scale(0.9); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# Imports from core
from core.pdf_handler import extract_text_from_pdf, generate_pdf_from_text
from core.humanizer import humanize_document
from core.plagiarism import check_plagiarism_document

# Automatically load the API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if api_key:
    # Ensure GEMINI_API_KEY is populated for the google-genai SDK
    os.environ["GEMINI_API_KEY"] = api_key

st.sidebar.markdown("### 🛠️ Mode Selection")
mode = st.sidebar.radio(
    "Select Capability",
    ["📝 AI Text Humanizer", "🔍 Plagiarism Checker"],
    index=0
)

# Optional: Advanced settings tucked away in an expander
with st.sidebar.expander("⚙️ Advanced Settings"):
    model_choice = st.selectbox(
        "Gemini Model",
        ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-1.5-flash"],
        index=0,
        help="gemini-2.5-flash is highly recommended for speed and search accuracy."
    )

# Shared UI Elements (Input Panel)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<h3 style="color: #F3F4F6; font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;"><span>📥</span> Source Text Input</h3>', unsafe_allow_html=True)

input_option = st.radio("Choose Input Source", ["Upload PDF File", "Paste Raw Text"], horizontal=True)

extracted_text = ""
file_name_label = ""

if input_option == "Upload PDF File":
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    if uploaded_file is not None:
        file_name_label = uploaded_file.name
        with st.spinner("Extracting text from PDF..."):
            try:
                pages_data = extract_text_from_pdf(uploaded_file)
                total_pages = len(pages_data)
                extracted_text = "\n\n".join([page["text"] for page in pages_data])
                st.success(f"Successfully extracted text from {total_pages} pages ({len(extracted_text.split())} words).")
            except Exception as e:
                st.error(f"Error reading PDF: {str(e)}")
else:
    extracted_text = st.text_area("Paste your text here (No word limit)", height=300, placeholder="Paste your AI-generated or draft text here...")

st.markdown('</div>', unsafe_allow_html=True)

# Mode Specific Configurations & Execution
if mode == "📝 AI Text Humanizer":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #F3F4F6; font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;"><span>🎨</span> Humanizer Configuration</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox(
            "Writing Tone & Style",
            ["Natural/Default", "Casual/Conversational", "Professional/Business", "Academic/Scholarly", "Creative/Expressive"],
            index=0,
            help="Select the style the humanized output should match."
        )
    with col2:
        intensity = st.select_slider(
            "Rewrite Intensity",
            options=["Light", "Medium", "High"],
            value="Medium",
            help="High does deeper restructuring, Light does mild correction."
        )
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process Button
    if st.button("🚀 Humanize Content"):
        if not extracted_text.strip():
            st.warning("Please provide some text to humanize.")
        elif not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            st.error("❌ Gemini API Key not found. Please set the GEMINI_API_KEY environment variable on your system or create a `.env` file containing `GEMINI_API_KEY=your_key` in the project folder.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total):
                progress_bar.progress(current / total)
                status_text.text(f"Processing chunk {current} of {total}...")
                
            try:
                with st.spinner("Humanizing AI content..."):
                    humanized_text = humanize_document(
                        text=extracted_text,
                        api_key=os.environ.get("GEMINI_API_KEY"),
                        tone=tone,
                        intensity=intensity,
                        model_name=model_choice,
                        progress_callback=update_progress
                    )
                
                status_text.text("Finished processing successfully!")
                
                # Results Section
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: #F3F4F6; font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;"><span>✨</span> Humanization Output</h3>', unsafe_allow_html=True)
                
                # Metrics
                orig_words = len(extracted_text.split())
                new_words = len(humanized_text.split())
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Original Word Count", orig_words)
                m2.metric("Humanized Word Count", new_words)
                m3.metric("Estimated Read Time", f"{max(1, round(new_words / 200))} min")
                
                # Side by Side comparison
                st.markdown("#### 🔄 Side-by-Side Comparison")
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Original Text**")
                    st.markdown(f'<div class="compare-column">{extracted_text.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                with c2:
                    st.markdown("**Humanized Text**")
                    st.markdown(f'<div class="compare-column">{humanized_text.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Downloads
                st.markdown("#### 📥 Download Results")
                dl_col1, dl_col2 = st.columns(2)
                
                with dl_col1:
                    st.download_button(
                        label="Download as Plain Text (.txt)",
                        data=humanized_text,
                        file_name="humanized_content.txt",
                        mime="text/plain"
                    )
                with dl_col2:
                    # Generate PDF bytes
                    try:
                        pdf_bytes = generate_pdf_from_text(humanized_text)
                        st.download_button(
                            label="Download as PDF (.pdf)",
                            data=pdf_bytes,
                            file_name="humanized_content.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Could not generate PDF download: {str(e)}")
                        
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred during humanization: {str(e)}")

else: # Plagiarism Checker
    if st.button("🔎 Scan for Plagiarism"):
        if not extracted_text.strip():
            st.warning("Please provide some text to scan.")
        elif not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
            st.error("❌ Gemini API Key not found. Please set the GEMINI_API_KEY environment variable on your system or create a `.env` file containing `GEMINI_API_KEY=your_key` in the project folder.")
        else:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total):
                progress_bar.progress(current / total)
                status_text.text(f"Scanning chunk {current} of {total} via Google Search...")
                
            try:
                with st.spinner("Analyzing text and querying Google Search..."):
                    report = check_plagiarism_document(
                        text=extracted_text,
                        api_key=os.environ.get("GEMINI_API_KEY"),
                        model_name=model_choice,
                        progress_callback=update_progress
                    )
                
                status_text.text("Scanning complete!")
                
                # Results Section
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown('<h3 style="color: #F3F4F6; font-size: 1.25rem; font-weight: 700; margin-top: 0; margin-bottom: 20px; display: flex; align-items: center; gap: 8px;"><span>📊</span> Plagiarism Report</h3>', unsafe_allow_html=True)
                
                score = report.get("similarity_score", 0)
                
                # Style meter color based on score
                if score < 15:
                    meter_color = "#48BB78" # Green
                    status_lbl = "Safe"
                    desc = "Very low similarity detected. Your content is highly unique."
                elif score < 35:
                    meter_color = "#ECC94B" # Yellow
                    status_lbl = "Caution"
                    desc = "Moderate similarity detected. Some phrases or sentences match existing online sources."
                else:
                    meter_color = "#F56565" # Red
                    status_lbl = "High Risk"
                    desc = "High similarity detected! Large portions of this text match existing online content."
                
                # Score Layout
                sc1, sc2 = st.columns([1, 2])
                with sc1:
                    st.markdown(f"<h1 style='text-align: center; color: {meter_color}; font-size: 5rem; margin-bottom: 0;'>{score}%</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-weight: bold; font-size: 1.2rem; color: {meter_color};'>{status_lbl}</p>", unsafe_allow_html=True)
                with sc2:
                    st.markdown(f"**Analysis Summary**")
                    st.markdown(desc)
                    st.markdown(f"**Explanation**: {report.get('explanation', 'No detailed explanation provided.')}")
                
                # Custom Progress Meter
                st.markdown(f"""
                <div class="meter-container">
                    <div class="meter-fill" style="width: {score}%; background-color: {meter_color};"></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Sources Section
                matches = report.get("matches", [])
                st.markdown(f"#### 🌐 Matched Web Sources ({len(matches)})")
                
                if matches:
                    for idx, match in enumerate(matches):
                        conf = match.get("confidence", 0)
                        card_class = "danger" if conf > 35 else ("warning" if conf > 15 else "")
                        st.markdown(f"""
                        <div class="source-card {card_class}">
                            <strong>{idx+1}. <a href="{match.get('source_url')}" target="_blank">{match.get('source_title', 'Unknown Title')}</a></strong><br>
                            <span style="color: #A0AEC0; font-size: 0.9rem;">Match Confidence: {conf}% | URL: {match.get('source_url')}</span><br>
                            <em style="color: #CBD5E0; font-size: 0.95rem;">Matched Text segment: "{match.get('text')}"</em>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No matching web sources found on Google Search.")
                
                st.markdown("---")
                
                # Highlighted Document Comparison
                st.markdown("#### 🔎 Highlighted Document Analysis")
                st.markdown("Below is your text with potential plagiarism matches highlighted. Click on web sources above to review the source material.")
                
                # Reconstruct document with highlighted sentences
                # We can approximate this by splitting the text into sentences
                # and checking if any sentence has a substring match in the plagiarized matches list.
                sentences = re.split(r'(?<=[.!?])\s+', extracted_text)
                highlighted_html = ""
                
                for sent in sentences:
                    sent_clean = sent.strip()
                    if not sent_clean:
                        continue
                        
                    is_match = False
                    matching_url = ""
                    
                    # Search matches list for overlaps
                    for m in matches:
                        m_text = m.get("text", "").strip()
                        # If the sentence overlaps significantly with matching text
                        if len(m_text) > 10 and (m_text.lower() in sent_clean.lower() or sent_clean.lower() in m_text.lower()):
                            is_match = True
                            matching_url = m.get("source_url")
                            break
                            
                    if is_match:
                        highlighted_html += f'<span class="plagiarized-text" title="Source: {matching_url}">{sent}</span> '
                    else:
                        highlighted_html += f'<span class="original-text">{sent}</span> '
                
                # Render highlighted text
                st.markdown(f'<div class="compare-column" style="height: auto; max-height: 500px;">{highlighted_html}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred during plagiarism scanning: {str(e)}")
