# Hive AI (Gift Recommendation API)

Hive AI is a standalone FastAPI backend for gift recommendations. It uses a rule-based tag engine, product matching, ranking logic, and a feedback loop to improve recommendation quality over time.

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

scripts/
  import_products.py
  update_scores.py
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

## API endpoints

- `GET /` health check
- `GET /products` list product catalog
- `POST /recommend` recommend gifts
- `POST /feedback` collect thumbs up/down feedback

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
  "rating": 1
}
```

## Notes

- Data is file-backed (`data/products.json` and `data/feedback.json`).
- AI/LLM integration is intentionally excluded from v1 and can be added later.
