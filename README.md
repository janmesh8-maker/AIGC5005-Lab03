# TV Show Summary – Lab 03

**Course:** AIGC5005 – Artificial Intelligence Capstone Project Preparation  
**Student:** Janmesh  
**Lab:** 03 – Refactor into a Package

## Project Overview

This project uses Python to download TV show information from the TVmaze API and generate a JSON summary. It counts shows by genre, calculates average ratings by language, and handles missing or invalid data.

For Lab 03, I converted my original Lab 02 program into a Python package using classes, inheritance, and separate modules.

## Data Source

- **API:** https://api.tvmaze.com/shows?page=0
- **Source:** TVmaze
- **Records:** Approximately 240 TV shows
- **One record:** Information about a single TV show, including its name, genres, language, and rating.

## Setup

Create and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate recordsummary
```

Install the dependencies and package:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Run

Run the program:

```bash
python main.py
```

The program downloads TV show information and saves the results to:

`data/processed/summary.json`

## Test

Run the unit tests:

```bash
python -m unittest discover -s tests
```

The tests check valid TV show records, invalid ratings, and missing genres without using the internet.

## Layout

- `main.py` – Starts the program and handles errors.
- `config.py` – Stores the API URL, timeout, and output path.
- `models.py` – Contains the TVShow class and cleans individual records.
- `sources.py` – Downloads records and converts them into TVShow objects.
- `aggregations.py` – Contains the base aggregation class and subclasses for genre counts and language ratings.
- `report.py` – Builds the summary and writes the JSON output.
- `__init__.py` – Exports the public classes and functions.
- `tests/test_models.py` – Contains unit tests.
- `environment.yml` – Defines the Conda environment.
- `requirements.txt` – Lists pinned Python dependencies.
- `pyproject.toml` – Defines the installable Python package.

## What moved where

| Lab 02 function or code | Lab 03 location |
|---|---|
| `SOURCE_URL` and `OUTPUT` | `config.py` |
| `fetch_records()` | `TVShowSource.fetch()` in `sources.py` |
| Record validation and cleaning | `TVShow.__init__()` in `models.py` |
| `shows_per_genre()` | `GenreAggregation.compute()` in `aggregations.py` |
| `average_rating_by_language()` | `RatingAggregation.compute()` in `aggregations.py` |
| `build_summary()` | `build_summary()` in `report.py` |
| `write_summary()` | `write_summary()` in `report.py` |
| `main()` | `main.py` |

## Design Choices

I separated the program into modules so that each part has a specific responsibility.

The `TVShow` class represents one TV show and cleans its values when an object is created. This makes it easier to handle missing or invalid data.

The `TVShowSource` class handles downloading the data and creating TVShow objects.

I used inheritance in `aggregations.py`. The `Aggregation` base class defines a common `compute()` method, while `GenreAggregation` and `RatingAggregation` override it to perform different calculations.

The summary builder loops through these aggregation objects without checking their class. This demonstrates polymorphism.

If I wanted to add another calculation, I could create another subclass of `Aggregation`, implement its `compute()` method, and add it to the list in `report.py`.

## Known Limitations

- The program requires an internet connection to download fresh data.
- The TVmaze API must be available.
- The program currently downloads only the first page of TV show records.
- The tests use handmade records and do not cover every possible API response.

## Conclusion

In this lab, I learned how to turn a single Python script into an organized and installable package. I practiced using classes, inheritance, modules, Conda environments, and unit testing while keeping the original program's functionality.