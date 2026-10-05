# AtlasTrade — complete starter platform

**CEO: Natnael Negash**

This package is a real Flask trading-platform foundation with authentication, database models, dashboard, chart UI, journal, API endpoints, rate limiting, admin page, and production configuration.

## Run locally

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python run.py
```

Open http://127.0.0.1:5000

The demo market endpoint intentionally uses deterministic sample candles. For live trading use, connect a properly licensed market-data provider through the adapter in `app/api.py`.

## Production

Use PostgreSQL via `DATABASE_URL`, set a strong `SECRET_KEY`, change the initial admin password immediately, and run:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

## Important

Broker execution, MT5 synchronization, payment processing, email delivery, and live market feeds require credentials and provider configuration. The project is structured so those adapters can be connected without exposing secrets in source code.

## Plans

AtlasTrade includes Basic, Pro and **Prime** plan presentation. Payment-provider checkout still requires the merchant account credentials and configuration.


## Payment setup

The application never asks for or stores your bank details. Use a payment processor/merchant account and configure its secret key, webhook secret, and recurring price IDs in `.env`. The processor then pays out to your verified bank account.

Configure:
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_BASIC`
- `STRIPE_PRICE_PRO`
- `STRIPE_PRICE_PRIME`

Real payment activation requires implementing the processor checkout and signed webhook handler with your merchant account. Never put secret keys in frontend JavaScript or Git.
