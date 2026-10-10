import json
from pathlib import Path

import requests


SOURCE_URL = "https://api.tvmaze.com/shows?page=0"
OUTPUT = Path(__file__).resolve().parent / "summary.json"


def fetch_records(url):
    """Download a JSON list of records with a request timeout."""
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    records = response.json()

    if not isinstance(records, list):
        raise ValueError("The API response must be a list of records.")

    return records


def shows_per_genre(records):
    """Count shows by valid genre and report missing or invalid genres."""
    counts = {}
    without_genres = 0
    invalid_entries = 0

    for show in records:
        genres = show.get("genres")

        if not isinstance(genres, list):
            without_genres += 1
            continue

        # Count a show only once within each genre.
        valid_genres = {
            genre.strip()
            for genre in genres
            if isinstance(genre, str) and genre.strip()
        }

        invalid_entries += sum(
            1
            for genre in genres
            if not isinstance(genre, str) or not genre.strip()
        )

        if not valid_genres:
            without_genres += 1
            continue

        for genre in valid_genres:
            counts[genre] = counts.get(genre, 0) + 1

    return {
        "counts": dict(sorted(counts.items())),
        "shows_without_valid_genres": without_genres,
        "invalid_genre_entries": invalid_entries,
    }


def average_rating_by_language(records):
    """Average valid ratings by language and report excluded shows."""
    groups = {}
    missing_language = 0
    invalid_rating = 0

    for show in records:
        language = show.get("language")

        if not isinstance(language, str) or not language.strip():
            missing_language += 1
            continue

        language = language.strip()

        if language not in groups:
            groups[language] = {
                "rating_total": 0,
                "rated_shows": 0,
            }

        rating_object = show.get("rating")
        rating = (
            rating_object.get("average")
            if isinstance(rating_object, dict)
            else None
        )

        # Missing and invalid ratings are excluded, not replaced with zero.
        if (
            isinstance(rating, bool)
            or not isinstance(rating, (int, float))
            or not 0 <= rating <= 10
        ):
            invalid_rating += 1
            continue

        groups[language]["rating_total"] += rating
        groups[language]["rated_shows"] += 1

    averages = {
        language: {
            "average_rating": (
                round(values["rating_total"] / values["rated_shows"], 2)
                if values["rated_shows"] > 0
                else None
            ),
            "rated_shows": values["rated_shows"],
        }
        for language, values in sorted(groups.items())
    }

    return {
        "languages": averages,
        "shows_without_valid_language": missing_language,
        "shows_with_language_but_without_valid_rating": invalid_rating,
    }


def build_summary(records):
    """Combine valid records, quality counts, and both aggregations."""
    valid_records = [
        record for record in records if isinstance(record, dict)
    ]

    if len(valid_records) < 50:
        raise ValueError(
            f"At least 50 usable records are required; "
            f"received {len(valid_records)}."
        )

    return {
        "source_url": SOURCE_URL,
        "records_downloaded": len(records),
        "records_processed": len(valid_records),
        "malformed_records_skipped": len(records) - len(valid_records),
        "shows_per_genre": shows_per_genre(valid_records),
        "average_rating_by_language": average_rating_by_language(
            valid_records
        ),
    }


def write_summary(summary, path):
    """Write the summary as indented UTF-8 JSON using pathlib."""
    path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
            allow_nan=False,
        ),
        encoding="utf-8",
    )


def main():
    """Download records, build the summary, and report the result."""
    try:
        records = fetch_records(SOURCE_URL)
    except requests.exceptions.RequestException:
        print(
            "Download failed. Check your internet connection "
            "and whether the TVmaze API is available."
        )
        return 1
    except ValueError as error:
        print(f"Invalid API data: {error}")
        return 1

    try:
        summary = build_summary(records)
    except ValueError as error:
        print(f"Cannot summarize the data: {error}")
        return 1

    try:
        write_summary(summary, OUTPUT)
    except (OSError, ValueError) as error:
        print(f"Could not save the summary: {error}")
        return 1

    print(f"Processed {summary['records_processed']} TV shows.")
    print(f"Summary saved to {OUTPUT.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())