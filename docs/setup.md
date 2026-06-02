# Setup Guide

## 1. Environment
Create a `.env` file from `.env.example` and set the values for:
- `BOT_TOKEN`
- `OPENAI_API_KEY`
- `TELEGRAM_ADMIN_IDS`
- `AZURE_CLIENT_ID`
- `AZURE_CLIENT_SECRET`
- `AZURE_TENANT_ID`
- `SHAREPOINT_SITE_ID`

## 2. Dependencies
Install the project requirements:

```bash
python3 -m pip install -r requirements.txt
```

## 3. Run locally
```bash
python3 main.py
```

## 4. Tests
```bash
python3 -m pytest -q
```
