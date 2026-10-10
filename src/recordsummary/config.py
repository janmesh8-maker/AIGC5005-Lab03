from pathlib import Path

# TVmaze API URL
SOURCE_URL = "https://api.tvmaze.com/shows?page=0"

# Download timeout in seconds
TIMEOUT = 30

# Project folder
BASE_DIR = Path(__file__).resolve().parents[2]

# Output file location
OUTPUT = BASE_DIR / "data" / "processed" / "summary.json"