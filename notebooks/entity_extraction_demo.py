"""
Entity Extraction Demo
Author: Andy Kowal | 33NGroup
Purpose: Compare spaCy and LLM-based extraction for multilingual text.
"""

import spacy
from openai import OpenAI

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Example text
text = "Juan Pérez met with Dr. Sarah Smith in Madrid to discuss a contract with Vision Analytics."

# --- spaCy Extraction ---
doc = nlp(text)
spacy_entities = [(ent.text, ent.label_) for ent in doc.ents]
print("spaCy Entities:", spacy_entities)

# --- LLM Extraction (requires OPENAI_API_KEY env var) ---
client = OpenAI()

prompt = f"Extract and label entities (people, orgs, locations) from this text:\n\n{text}"
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
)
llm_output = response.choices[0].message.content
print("\nLLM Entities:\n", llm_output)

# --- Example Output Format ---
# spaCy Entities: [('Juan Pérez', 'PERSON'), ('Sarah Smith', 'PERSON'), ('Madrid', 'GPE'), ('Vision Analytics', 'ORG')]
# LLM Entities: { "people": ["Juan Pérez", "Sarah Smith"], "organizations": ["Vision Analytics"], "locations": ["Madrid"] }
