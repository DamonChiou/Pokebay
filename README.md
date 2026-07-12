# PokeBay API

A personal deal-finder that monitors eBay listings for underpriced Pokemon cards by comparing eBay prices against TCGPlayer market prices. When a listing is significantly below market value, it sends an email alert.

---

## How It Works

```
eBay API → ingest raw listings → fuzzy match to product catalog → compare vs TCGPlayer price → email alert if deal found
```

1. The ingestion pipeline fetches live eBay listings and saves them raw to the database
2. The matcher links each listing to a known product using fuzzy title matching
3. The deal scorer compares the listing price against the TCGPlayer market price
4. If the listing is below the threshold, an email alert is sent via Resend

---

## Architecture

```
src/pokebay/
├── config.py              reads all credentials from .env
├── db/
│   ├── base.py            SQLAlchemy Base class (model registry)
│   ├── engine.py          database connection + session factory
│   └── models/
│       ├── product.py     products table (reference data — cards, boxes, packs)
│       └── listing.py     listings table (transactional — raw eBay listings)
├── clients/
│   ├── ebay.py            eBay Browse API client (OAuth + search)
│   └── tcgplayer.py       TCGPlayer API client (market prices)
├── ingestion/
│   └── runner.py          orchestrates clients, saves data to DB on a schedule
├── matching/
│   └── matcher.py         fuzzy matches raw listing titles to known products
├── scoring/
│   └── deal_scorer.py     compares listing price vs TCGPlayer market price
└── alerts/
    └── email.py           sends deal alert emails via Resend API
```

---

## Database Schema

**`products`** — reference table of known Pokemon items
| Column | Type | Description |
|---|---|---|
| id | integer | primary key |
| name | varchar | card/product name |
| product_type | varchar | "card", "box", "pack" |
| set_name | varchar | e.g. "Sword & Shield" |
| tcg_market_price | numeric | current TCGPlayer market price |
| tcg_product_id | varchar | TCGPlayer's internal ID |

**`listings`** — live eBay listings scraped by the pipeline
| Column | Type | Description |
|---|---|---|
| id | integer | primary key |
| ebay_listing_id | varchar | eBay's unique listing ID |
| raw_title | text | listing title exactly as eBay returns it |
| price | numeric | buy-it-now price |
| url | text | direct link to listing |
| scraped_at | timestamp | when this listing was fetched |
| product_id | integer (FK) | matched product (NULL if unmatched) |

---

## Stack

- **Language:** Python 3.13
- **Web framework:** FastAPI
- **Database:** PostgreSQL (local via Homebrew, migrations via Alembic)
- **ORM:** SQLAlchemy 2.0 (async)
- **HTTP client:** httpx (async)
- **Fuzzy matching:** rapidfuzz
- **Scheduler:** APScheduler
- **Email:** Resend API
- **Frontend:** React (planned)

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/pokebay-api.git
cd pokebay-api

# 2. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e .

# 4. Copy environment variables and fill in your credentials
cp .env.example .env

# 5. Run database migrations
alembic upgrade head

# 6. Start the API server
uvicorn pokebay.main:app --reload
```

---

## Environment Variables

```
DATABASE_URL=postgresql+asyncpg://localhost/pokebay
EBAY_APP_ID=your-ebay-app-id
EBAY_CLIENT_SECRET=your-ebay-cert-id
TCGPLAYER_PUBLIC_KEY=your-tcgplayer-public-key
TCGPLAYER_PRIVATE_KEY=your-tcgplayer-private-key
RESEND_API_KEY=your-resend-api-key
ALERT_EMAIL_TO=your-email@example.com
```

---

## Build Progress

- [x] Database layer (models, migrations)
- [ ] eBay API client
- [ ] TCGPlayer API client
- [ ] Ingestion pipeline
- [ ] Matching layer
- [ ] Deal scoring
- [ ] Alert system
- [ ] FastAPI routes
- [ ] React dashboard
