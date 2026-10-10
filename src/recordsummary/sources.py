from dbm import error
from urllib import response

import requests
from .models import TVShow


class TVShowSource:
    """Downloads TV shows and converts them into TVShow objects."""

    def __init__(self, url, timeout=30):
        self.url = url
        self.timeout = timeout
        self.records_downloaded = 0
        self.malformed_records_skipped = 0

    def fetch(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()

        except requests.exceptions.RequestException as error:
            raise ConnectionError(
        "Download failed. Check your internet connection "
        "and whether the TVmaze API is available."
    ) from error

        data = response.json()

        if not isinstance(data, list):
            raise ValueError("The API response must be a list of records.")

        self.records_downloaded = len(data)
        self.malformed_records_skipped = 0
        shows = []

        for record in data:
            if isinstance(record, dict):
                shows.append(TVShow(record))
            else:
                self.malformed_records_skipped += 1

        return shows