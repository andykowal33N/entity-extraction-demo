# Sample Data Pack — entity-extraction-demo

All data is **synthetic** and safe for public use.

## Files

- `customer_records.csv` — tabular CRM-like rows (names, emails, phones, addresses).
- `news_articles.jsonl` — one JSON object per line with short news snippets.
- `chat_transcripts.jsonl` — synthetic two-message helpdesk-style chats.
- `sanctions_list.csv` — tiny, toy sanctions-style lookup with aliases.
- `resumes/` — three plain-text resume snippets.
- `gold_labels/` — toy gold labels for a couple of sources to demo eval.

## Suggested Tasks

- NER on `news_articles.jsonl` and `chat_transcripts.jsonl`.
- PII extraction + validation on `customer_records.csv`.
- Alias resolution using `sanctions_list.csv` and `resumes/`.
- Simple precision/recall against `gold_labels/` (example only).

## License

CC0-1.0 — Public-domain dedication for this sample pack.

Generated on 2025-11-11.
