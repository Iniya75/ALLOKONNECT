"""
WriterAgent — Generate a professional ~300-word news article via Gemini.

Uses the new google-genai SDK (google.genai).

Returns JSON:
{
    "title":       "...",
    "summary":     "~300-word AI article",
    "description": "Short teaser / lead paragraph"
}
"""

import os
import json
import re
from dotenv import load_dotenv

from google import genai

load_dotenv()

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class WriterAgent:

    def rewrite(self, article: dict) -> dict:
        """
        Generate original AI content for the given article.
        Falls back to the original description if Gemini fails.
        """
        title       = article.get("title", "")
        description = article.get("description", "")
        content     = article.get("content", description)

        print(f"[WriterAgent] Generating AI article for: {title}")

        try:
            prompt = f"""You are a professional technology journalist writing for a premium news website similar to TechCrunch or The Verge.

Write a completely original news article based on the information below.
Do NOT copy the source text. Write your own original journalistic piece.
Do NOT mention Reuters, GNews, CNN, BBC, AP, or any news provider name.
Do NOT use markdown formatting (no **, no ##, no bullet points with -).
Write in plain flowing paragraphs only.

The article must be approximately 300 words and cover:
1. Introduction — Hook the reader with the key fact
2. Background — Context and history
3. What happened — The core news
4. Why it matters — Significance for readers/industry
5. Future impact — What comes next

Return ONLY valid JSON in this exact format (no markdown, no code fences):
{{
    "title": "compelling headline (max 12 words)",
    "summary": "the full ~300-word article written in plain paragraphs",
    "description": "a single teaser sentence of 25-40 words for the card preview"
}}

Source title: {title}
Source description: {description}
"""

            response = _client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )

            raw = response.text.strip()

            # Strip any accidental markdown fences
            raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
            raw = re.sub(r"\s*```$",          "", raw, flags=re.MULTILINE)
            raw = raw.strip()

            result = json.loads(raw)

            if not all(k in result for k in ("title", "summary", "description")):
                raise ValueError("Missing required JSON keys")

            print("[WriterAgent] AI article generated successfully")
            return result

        except Exception as e:
            print(f"[WriterAgent] Gemini failed ({e}) - using original content as fallback")
            return {
                "title":       title,
                "summary":     description or content,
                "description": (description or content)[:200],
            }