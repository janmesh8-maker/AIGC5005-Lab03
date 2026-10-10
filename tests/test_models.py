import unittest
from unittest.mock import patch
import requests

from recordsummary.models import TVShow
from recordsummary.sources import TVShowSource


class TestTVShow(unittest.TestCase):
    """Tests for the TVShow class."""

    def test_valid_show(self):
        data = {
            "name": "Breaking Bad",
            "genres": ["Drama", "Crime"],
            "language": "English",
            "rating": {"average": 9.5}
        }

        show = TVShow(data)

        self.assertEqual(show.name, "Breaking Bad")
        self.assertEqual(show.rating, 9.5)
        self.assertIn("Drama", show.genres)

    def test_invalid_rating(self):
        data = {
            "name": "Test Show",
            "genres": ["Comedy"],
            "language": "English",
            "rating": {"average": 15}
        }

        show = TVShow(data)

        self.assertIsNone(show.rating)

    def test_missing_genres(self):
        data = {
            "name": "Another Show",
            "genres": None,
            "language": "English",
            "rating": {"average": 8}
        }

        show = TVShow(data)

        self.assertEqual(show.genres, set())

    def test_download_failure(self):
        source = TVShowSource("https://example.com")

        with patch(
            "recordsummary.sources.requests.get",
            side_effect=requests.exceptions.ConnectionError()
        ):
            with self.assertRaises(ConnectionError):
                source.fetch()


if __name__ == "__main__":
    unittest.main()