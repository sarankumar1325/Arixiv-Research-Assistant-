# API Keys Required

This application requires API keys to function. Here's what you need:

## Required API Keys

### 1. Google API Key (REQUIRED)
**Purpose:** Access to Google's Gemini 2.0 Flash model for AI analysis and report generation

**How to get it:**
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key

**Cost:** Google offers a free tier with generous limits (check current pricing at [Google AI pricing](https://ai.google.dev/pricing))

## Optional API Keys

Currently, this application only requires the Google API Key. The arXiv API does not require authentication for basic usage.

## Setting Up Your Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. Never commit `.env` to version control (it's already in `.gitignore`)

## Using uv for Package Management

This project now uses [uv](https://github.com/astral-sh/uv) for fast Python package management.

### Installation

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Running the Application with uv

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Run the web interface:**
   ```bash
   uv run python app.py
   ```

3. **Or run the CLI version:**
   ```bash
   uv run python start_cli.py
   ```

### Alternative: Using pip

If you prefer not to use uv:
```bash
pip install -e .
```
