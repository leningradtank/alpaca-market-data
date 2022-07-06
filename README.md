# Pulling Market Data
Pulling SPY data using Alpaca Market Data API and uploading to a GCS bucket

Docker image copies over the app.py script and runs it. App.py pulls SPY data and can act as a backfill tenplate from a specified date for a specific symbol.
