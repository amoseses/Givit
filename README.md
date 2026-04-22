# Hive AI (Gift Recommendation API)

Hive AI is a standalone FastAPI backend for gift recommendations. It now behaves like a lightweight self-improving system: recommendations are ranked with weighted signals, feedback updates scores immediately, and behavior metrics are persisted over time.

## Project structure

```text
backend/
  main.py
  api/
    recommend.py
    feedback.py
    products.py
  core/
    tag_engine.py
    matcher.py
    ranker.py
  models/
    product.py
    user.py
  db/
    database.py
    seed.py
  utils/
    scoring.py

data/
  products.json
  feedback.json
  metrics.json
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
uvicorn backend.main:app --reload --port 8000
```

On startup the app automatically initializes `data/products.json`, `data/feedback.json`, and `data/metrics.json` when missing.

## API endpoints

- `GET /` health check
- `GET /products` list product catalog
- `GET /metrics` show learning-performance history
- `POST /recommend` recommend gifts and track product views
- `POST /feedback` register click/positive/negative feedback and update rankings instantly

### Example request: `/recommend`

```json
{
  "relationship": "mom",
  "interest": "cooking",
  "budget": 50,
  "occasion": "birthday"
}
```

### Example request: `/feedback`

```json
{
  "product_id": 1,
  "action": "positive"
}
```

## Learning details

- Product-level learning metrics are persisted per item:
  - `views`
  - `clicks`
  - `positive_feedback`
  - `negative_feedback`
- Learned score formula:
  - `(positive_feedback * 2 + clicks) / (views + negative_feedback + 1)`
- Final recommendation score:
  - `0.5 * match_score + 0.3 * learned_score + 0.2 * budget_score`
- Metrics history tracks:
  - average top-5 recommendation score
  - positive feedback ratio over total feedback events

## Notes

- Data is file-backed and uses atomic writes for persistence safety.
- Tag extraction is pluggable via `rule_based_tags` and an `ai_generated_tags` stub for future LLM integration.
