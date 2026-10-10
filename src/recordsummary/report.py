import json

from .config import SOURCE_URL, OUTPUT
from .aggregations import GenreAggregation, RatingAggregation


def build_summary(shows, records_downloaded):
    """Build the TV show summary using aggregation classes."""

    if len(shows) < 50:
        raise ValueError(
            f"At least 50 usable records are required; "
            f"received {len(shows)}."
        )

    summary = {
        "source_url": SOURCE_URL,
        "records_downloaded": records_downloaded,
        "records_processed": len(shows),
        "malformed_records_skipped": records_downloaded - len(shows)
    }

    # Run both aggregations using polymorphism
    aggregations = [
        GenreAggregation(),
        RatingAggregation()
    ]

    for aggregation in aggregations:
        summary[aggregation.name] = aggregation.compute(shows)

    return summary


def write_summary(summary, path=OUTPUT):
    """Save the summary as a formatted JSON file."""

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            summary,
            indent=2,
            ensure_ascii=False,
            allow_nan=False
        ),
        encoding="utf-8"
    )