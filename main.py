

from recordsummary.config import SOURCE_URL, TIMEOUT, OUTPUT
from recordsummary.sources import TVShowSource
from recordsummary.report import build_summary, write_summary


def main():
    """Run the TV show summary program."""

    source = TVShowSource(SOURCE_URL, TIMEOUT)

    try:
        shows = source.fetch()

    except ConnectionError as error:
        print(error)
        return 1

    except ValueError as error:
        print(f"Invalid API data: {error}")
        return 1

    try:
        summary = build_summary(
            shows,
            source.records_downloaded
        )

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