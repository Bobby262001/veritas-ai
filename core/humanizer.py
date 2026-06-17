from google import genai
from google.genai import types
import os
from utils.helpers import chunk_text, execute_with_retry

def get_humanizer_system_prompt(tone: str, intensity: str) -> str:
    """
    Generates a specialized system prompt for the humanizer based on tone and intensity.
    """
    tone_descriptions = {
        "Natural/Default": "Write in a natural, balanced, and engaging human voice. Avoid both overly formal and overly casual language.",
        "Casual/Conversational": "Write in a relaxed, friendly, and conversational tone. Use active voice, occasional contractions, and a warm, relatable style as if talking to a friend.",
        "Professional/Business": "Write in a polished, clear, and authoritative business tone. Maintain professionalism while ensuring the writing is active, concise, and free of corporate jargon or buzzwords.",
        "Academic/Scholarly": "Write in an analytical, precise, and intellectual tone. Maintain rigour and depth, but write with the clarity, flow, and sentence variety of a top-tier researcher rather than a rigid AI template.",
        "Creative/Expressive": "Write with artistic flair, using rich vocabulary, vivid imagery, and varied flow. Focus on storytelling, engagement, and emotional resonance."
    }
    
    selected_tone = tone_descriptions.get(tone, tone_descriptions["Natural/Default"])
    
    intensity_instructions = {
        "Light": "Apply subtle revisions. Keep most of the original sentence structure, but fix repetitive patterns, replace obvious AI-typical words, and smooth out transitions.",
        "Medium": "Apply moderate restructuring. Rewrite sentences for better flow, vary length dynamically, replace repetitive vocabulary, and significantly improve readability.",
        "High": "Perform a deep rewrite. Fully restructure sentences, rephrase ideas using natural human idioms, maximize sentence length variance (burstiness), and thoroughly eliminate all AI signatures."
    }
    
    selected_intensity = intensity_instructions.get(intensity, intensity_instructions["Medium"])
    
    prompt = f"""You are an expert copywriter, developmental editor, and professional human writer.
Your job is to rewrite the provided AI-generated text to make it read completely naturally, as if written by an experienced human writer.

### Style and Tone Requirements:
- **Tone**: {selected_tone}
- **Rewrite Intensity**: {selected_intensity}

### Key Rules for Human-Like Writing:
1. **Sentence Variety (Burstiness)**: Humans write with varied sentence lengths. Use very short sentences for impact, medium sentences for details, and longer, complex sentences for explanations. Do not make all sentences the same length.
2. **Vocabulary and Phrasing (Perplexity)**: Avoid predictable, typical AI word choices and transitions. 
   - DO NOT use words like: "delve", "testament", "tapestry", "moreover", "furthermore", "crucial", "essential", "not only... but also", "in conclusion", "it is important to note", "firstly/secondly", "beacon", "pinnacle".
   - Use natural transitions, active verbs, and normal vocabulary.
3. **Flow and Rhythm**: Ensure the paragraphs flow naturally from one point to the next. Use transitional phrases that feel spoken rather than written.
4. **Preserve Meaning**: Do not add new facts, change the core arguments, or lose the original meaning of the text. Keep all references, numbers, names, and core arguments intact.
5. **No AI Structural Markers**: Avoid bullet lists for simple narratives, and avoid starting every paragraph with a thematic transition word.

### Output format:
Return ONLY the rewritten humanized text. Do not include any introductory text, notes, or explanations (e.g., do not say "Here is your humanized text:").
"""
    return prompt

def humanize_chunk(text: str, client: genai.Client, tone: str, intensity: str, model_name: str = "gemini-2.5-flash") -> str:
    """
    Humanizes a single chunk of text.
    """
    system_prompt = get_humanizer_system_prompt(tone, intensity)
    
    def make_api_call(target_model):
        return client.models.generate_content(
            model=target_model,
            contents=text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.75,
                max_output_tokens=4000
            )
        )
        
    try:
        try:
            # Try primary model with 3 retries
            response = execute_with_retry(lambda: make_api_call(model_name), max_retries=3)
            return response.text.strip()
        except Exception as e:
            # Fall back if primary model fails
            fallback_model = "gemini-1.5-flash" if model_name != "gemini-1.5-flash" else "gemini-2.5-flash"
            response = execute_with_retry(lambda: make_api_call(fallback_model), max_retries=2)
            return response.text.strip()
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API: {str(e)}")

def humanize_document(text: str, api_key: str, tone: str = "Natural/Default", intensity: str = "Medium", model_name: str = "gemini-2.5-flash", progress_callback=None) -> str:
    """
    Splits the document into chunks, humanizes each chunk, and merges them.
    Includes a callback to report progress (for Streamlit progress updates).
    """
    # Initialize client
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        # Fallback to environment variable if client initialization permits
        client = genai.Client()
        
    chunks = chunk_text(text, max_words=700)
    total_chunks = len(chunks)
    humanized_chunks = []
    
    for idx, chunk in enumerate(chunks):
        if progress_callback:
            progress_callback(idx + 1, total_chunks)
            
        humanized_chunk = humanize_chunk(chunk, client, tone, intensity, model_name)
        humanized_chunks.append(humanized_chunk)
        
    return "\n\n".join(humanized_chunks)
