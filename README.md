# Email Access Checker

A production-ready Python project for validating and checking email account accessibility, provider detection, security posture, and batch processing.

## Features

- Email format validation
- Login credential checks with safe error handling
- IMAP/SMTP access verification
- Provider detection for Gmail, Outlook, Yahoo, ProtonMail, and custom IMAP
- 2FA / app-password guidance
- Batch processing with rate limiting
- CSV/JSON/Excel/HTML/PDF export
- REST API and CLI
- Dashboard with upload and analytics
- Secure logging and encryption
- SQLite-backed storage for results

## Quick start

1. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Copy environment settings

```bash
cp .env.example .env
```

4. Run a single validation

```bash
python main.py check --email user@gmail.com --password your_password
```

5. Run a batch file

```bash
python main.py batch --file examples/accounts.csv --output results.json
```

6. Start the API server

```bash
python main.py api
```

7. Or start the web dashboard

```bash
python main.py dashboard
```

## CLI examples

```bash
python main.py check --email user@gmail.com --password pass123
python main.py batch --file emails.csv --output results.json
python main.py schedule --file emails.csv --interval 24h
python main.py report --input results.json --format pdf
```

## API endpoints

- POST /api/check
- POST /api/batch
- GET /api/results
- GET /api/health
- POST /api/export

## Dashboard

Open the dashboard at:

- http://localhost:8000

The dashboard supports CSV/JSON upload, summary cards, filters, and export actions.

## Security notes

- Passwords are never printed in logs.
- Sensitive values are encrypted before storage.
- IMAP/SMTP connections use TLS/SSL when required.
- The project avoids brute-force patterns and rate-limit abuse protections.
- Use provider-specific app passwords where required.

## Provider support

- Gmail
- Outlook / Microsoft 365
- Yahoo
- ProtonMail
- Custom IMAP servers

## Environment variables

See `.env.example` for configuration.

## Testing

```bash
pytest -q
```

## Project structure

```text
src/
  core/
    email_checker.py
    providers/
      gmail.py
      outlook.py
      imap.py
      smtp.py
  validators/
    email_format.py
    security_checker.py
    breach_checker.py
  batch/
    processor.py
    scheduler.py
  ui/
    cli.py
    web/
      app.py
      api.py
  reporting/
    exporters.py
    generator.py
  utils/
    encryption.py
    config.py
    logging.py
  database/
    connection.py
    models.py
```

## Disclaimer

This project is intended for legitimate account validation and operational auditing in controlled, authorized environments. Always respect provider policies, service limits, and privacy requirements.
