import re

def chunk_text(text: str, max_words: int = 800) -> list:
    """
    Splits a single long string of text into logical chunks of approximately max_words.
    Keeps paragraphs intact where possible.
    """
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        words = para.split()
        word_count = len(words)
        
        if current_word_count + word_count > max_words and current_chunk:
            # Save the current chunk
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [para]
            current_word_count = word_count
        else:
            current_chunk.append(para)
            current_word_count += word_count
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    # Fallback: if a single paragraph is larger than max_words, split it by sentences
    final_chunks = []
    for chunk in chunks:
        words = chunk.split()
        if len(words) > max_words + 200:
            # Split paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', chunk)
            sub_chunk = []
            sub_count = 0
            for sent in sentences:
                sent_words = len(sent.split())
                if sub_count + sent_words > max_words and sub_chunk:
                    final_chunks.append(" ".join(sub_chunk))
                    sub_chunk = [sent]
                    sub_count = sent_words
                else:
                    sub_chunk.append(sent)
                    sub_count += sent_words
            if sub_chunk:
                final_chunks.append(" ".join(sub_chunk))
        else:
            final_chunks.append(chunk)
            
    return final_chunks

def chunk_pages(pages_data: list, max_words: int = 800) -> list:
    """
    Takes a list of page dicts: [{"page_number": int, "text": str}]
    and groups them into chunks of at most max_words, keeping track of page metadata.
    Returns a list of dicts: [{"chunk_id": int, "page_numbers": list[int], "text": str}]
    """
    chunks = []
    current_chunk_text = []
    current_word_count = 0
    current_pages = []
    chunk_id = 1
    
    for page in pages_data:
        p_num = page["page_number"]
        text = page["text"]
        
        # If the page itself is huge, split it using chunk_text
        page_words_count = len(text.split())
        if page_words_count > max_words:
            # First, flush current chunk if it exists
            if current_chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_numbers": list(current_pages),
                    "text": "\n\n".join(current_chunk_text)
                })
                chunk_id += 1
                current_chunk_text = []
                current_word_count = 0
                current_pages = []
            
            # Split the huge page into sub-chunks
            page_chunks = chunk_text(text, max_words)
            for pc in page_chunks:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_numbers": [p_num],
                    "text": pc
                })
                chunk_id += 1
        else:
            # If adding this page exceeds limit, flush first
            if current_word_count + page_words_count > max_words and current_chunk_text:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page_numbers": list(current_pages),
                    "text": "\n\n".join(current_chunk_text)
                })
                chunk_id += 1
                current_chunk_text = [text]
                current_word_count = page_words_count
                current_pages = [p_num]
            else:
                current_chunk_text.append(text)
                current_word_count += page_words_count
                if p_num not in current_pages:
                    current_pages.append(p_num)
                    
    if current_chunk_text:
        chunks.append({
            "chunk_id": chunk_id,
            "page_numbers": list(current_pages),
            "text": "\n\n".join(current_chunk_text)
        })
        
    return chunks

import time
import random

def execute_with_retry(api_call_func, max_retries: int = 3, initial_delay: float = 1.0):
    """
    Executes an API call with exponential backoff and jitter for transient errors (like 503 or 429).
    """
    delay = initial_delay
    for attempt in range(max_retries + 1):
        try:
            return api_call_func()
        except Exception as e:
            err_msg = str(e)
            is_retryable = (
                "503" in err_msg or 
                "429" in err_msg or 
                "UNAVAILABLE" in err_msg or 
                "ResourceExhausted" in err_msg or 
                "high demand" in err_msg.lower() or
                "overloaded" in err_msg.lower()
            )
            
            if is_retryable and attempt < max_retries:
                sleep_time = delay * random.uniform(0.8, 1.5)
                time.sleep(sleep_time)
                delay *= 2  # Exponential backoff
            else:
                raise e
