from google import genai
from google.genai import types
import json
import os
import re
from utils.helpers import chunk_text, execute_with_retry

def get_plagiarism_system_prompt() -> str:
    """
    Returns the system instruction prompt for the plagiarism checker.
    """
    prompt = """You are a highly advanced Plagiarism Detection System.
Your task is to check the provided text for plagiarism by searching the internet.
You must analyze the text paragraph-by-paragraph or sentence-by-sentence, search for identical or heavily paraphrased versions on the web, and report your findings.

You MUST respond ONLY with a JSON object. Do not include markdown code block backticks (like ```json ... ```) or any other text. The output must be pure, parsable JSON.

The JSON object must follow this schema:
{
  "similarity_score": 0, // Integer between 0 and 100 representing the overall plagiarism percentage for this text
  "is_plagiarized": false, // True if similarity_score is 15 or higher
  "explanation": "Brief explanation of the findings.",
  "matches": [
    {
      "text": "The specific phrase or sentence from the input text that matches an online source.",
      "source_title": "Title of the website or article found",
      "source_url": "URL of the matching web page",
      "confidence": 95 // Integer between 0 and 100 representing confidence of the match
    }
  ]
}

If no plagiarism or matching content is found, set similarity_score to 0, is_plagiarized to false, explanation to 'No matches found', and matches to an empty list [].
Be rigorous. Check for both exact text matches and close paraphrasing.
"""
    return prompt

def check_plagiarism_chunk(text: str, client: genai.Client, model_name: str = "gemini-2.5-flash") -> dict:
    """
    Checks a single chunk of text for plagiarism using Google Search Grounding.
    Combines the JSON output from the model and the actual grounding metadata from the search tool.
    """
    system_prompt = get_plagiarism_system_prompt()
    grounding_tool = types.Tool(google_search=types.GoogleSearch())
    
    config = types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[grounding_tool],
        temperature=0.1 # Low temperature for more deterministic/factual output
    )
    
    def make_api_call(target_model):
        return client.models.generate_content(
            model=target_model,
            contents=f"Analyze this text for plagiarism: \n\n{text}",
            config=config
        )
        
    try:
        try:
            # Try primary model with 3 retries
            response = execute_with_retry(lambda: make_api_call(model_name), max_retries=3)
        except Exception as e:
            # Fall back if primary model fails
            fallback_model = "gemini-1.5-flash" if model_name != "gemini-1.5-flash" else "gemini-2.5-flash"
            response = execute_with_retry(lambda: make_api_call(fallback_model), max_retries=2)
        
        # Parse the JSON response
        report = {}
        try:
            # Clean up the output string if the model accidentally wrapped it in code blocks
            res_text = response.text.strip()
            if res_text.startswith("```"):
                # Remove markdown fences
                res_text = re.sub(r'^```(?:json)?\n', '', res_text)
                res_text = re.sub(r'\n```$', '', res_text)
            report = json.loads(res_text)
        except Exception as e:
            # Fallback report if parsing fails
            report = {
                "similarity_score": 0,
                "is_plagiarized": False,
                "explanation": f"Failed to parse plagiarism report JSON: {str(e)}",
                "matches": []
            }
            
        # Extract grounding metadata as a secondary validation to get absolute verified URLs
        verified_sources = []
        candidate = response.candidates[0]
        if candidate.grounding_metadata:
            metadata = candidate.grounding_metadata
            if metadata.grounding_chunks:
                for chunk in metadata.grounding_chunks:
                    if chunk.web:
                        verified_sources.append({
                            "title": chunk.web.title,
                            "url": chunk.web.uri
                        })
                        
        # Merge verified grounding sources if they are not in the matches list
        existing_urls = {m.get("source_url") for m in report.get("matches", []) if m.get("source_url")}
        
        for vs in verified_sources:
            if vs["url"] not in existing_urls:
                # Add this source as a match if the model's similarity score was > 0
                if report.get("similarity_score", 0) > 0 and len(report.get("matches", [])) < 5:
                    report["matches"].append({
                        "text": "General matching content / context source",
                        "source_title": vs["title"],
                        "source_url": vs["url"],
                        "confidence": report.get("similarity_score")
                    })
                    
        return report
        
    except Exception as e:
        raise RuntimeError(f"Error calling Gemini API for plagiarism: {str(e)}")

def check_plagiarism_document(text: str, api_key: str, model_name: str = "gemini-2.5-flash", progress_callback=None) -> dict:
    """
    Checks an entire document for plagiarism by chunking it, checking each chunk,
    and aggregating the results.
    """
    if api_key:
        client = genai.Client(api_key=api_key)
    else:
        client = genai.Client()
        
    chunks = chunk_text(text, max_words=600) # Slightly smaller chunks for search grounding
    total_chunks = len(chunks)
    
    all_reports = []
    
    for idx, chunk in enumerate(chunks):
        if progress_callback:
            progress_callback(idx + 1, total_chunks)
            
        report = check_plagiarism_chunk(chunk, client, model_name)
        all_reports.append((chunk, report))
        
    # Aggregate reports
    total_similarity = 0
    all_matches = []
    explanations = []
    unique_urls = set()
    
    for chunk, report in all_reports:
        # Weighted average of similarity or maximum? Let's take the max similarity score across chunks
        # because if a single page is 100% plagiarized, the document has significant plagiarism.
        # But average also helps show the proportion. Let's do a weighted average or show both.
        # Actually, let's calculate: (Sum of (chunk_similarity * chunk_length)) / total_length
        chunk_words = len(chunk.split())
        total_similarity += report.get("similarity_score", 0) * chunk_words
        
        # Collect explanations
        exp = report.get("explanation", "")
        if exp and exp not in explanations:
            explanations.append(exp)
            
        # Collect matches
        for match in report.get("matches", []):
            url = match.get("source_url")
            if url and url not in unique_urls:
                unique_urls.add(url)
                all_matches.append(match)
                
    total_words = sum(len(c.split()) for c, _ in all_reports)
    avg_similarity = round(total_similarity / total_words) if total_words > 0 else 0
    
    # Cap similarity score at 100
    avg_similarity = min(avg_similarity, 100)
    
    aggregated_report = {
      "similarity_score": avg_similarity,
      "is_plagiarized": avg_similarity >= 15,
      "explanation": "; ".join(explanations[:3]),
      "matches": all_matches,
      "chunk_reports": [{"chunk_text": chunk, "report": rep} for chunk, rep in all_reports]
    }
    
    return aggregated_report
