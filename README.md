# FastAPI Review Sentiment Service

## Install & Run

```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

## Example: Add a Review

```bash
curl -X POST http://127.0.0.1:8000/reviews \
  -H "Content-Type: application/json" \
  -d '{"text": "Очень хороший сервис, люблю!"}'
```

**Response:**
```json
{
  "id": 1,
  "text": "Очень хороший сервис, люблю!",
  "sentiment": "positive",
  "created_at": "2025-07-11T12:34:56.789123"
}
```

## Example: Get All Reviews

```bash
curl http://127.0.0.1:8000/reviews
```

## Example: Get Only Negative Reviews

```bash
curl "http://127.0.0.1:8000/reviews?sentiment=negative"
```

**Response:**
```json
[
  {
    "id": 2,
    "text": "Очень плохо, ненавижу этот продукт.",
    "sentiment": "negative",
    "created_at": "2025-07-11T12:35:10.123456"
  }