class Aggregation:
    """Base class for TV show calculations."""

    def __init__(self, name):
        self.name = name

    def compute(self, shows):
        raise NotImplementedError("Subclasses must implement compute().")


class GenreAggregation(Aggregation):
    """Counts shows by genre."""

    def __init__(self):
        super().__init__("shows_per_genre")

    def compute(self, shows):
        counts = {}
        without_genres = 0
        invalid_entries = 0

        for show in shows:
            invalid_entries += show.invalid_genre_entries

            if not show.genres:
                without_genres += 1
                continue

            for genre in show.genres:
                counts[genre] = counts.get(genre, 0) + 1

        return {
            "counts": dict(sorted(counts.items())),
            "shows_without_valid_genres": without_genres,
            "invalid_genre_entries": invalid_entries
        }


class RatingAggregation(Aggregation):
    """Calculates average TV show ratings by language."""

    def __init__(self):
        super().__init__("average_rating_by_language")

    def compute(self, shows):
        groups = {}
        missing_language = 0
        invalid_rating = 0

        for show in shows:
            if show.language is None:
                missing_language += 1
                continue

            language = show.language

            if language not in groups:
                groups[language] = {
                    "rating_total": 0,
                    "rated_shows": 0
                }

            if show.rating is None:
                invalid_rating += 1
                continue

            groups[language]["rating_total"] += show.rating
            groups[language]["rated_shows"] += 1

        averages = {}

        for language, values in sorted(groups.items()):
            total = values["rating_total"]
            count = values["rated_shows"]

            if count > 0:
                average = round(total / count, 2)
            else:
                average = None

            averages[language] = {
                "average_rating": average,
                "rated_shows": count
            }

        return {
            "languages": averages,
            "shows_without_valid_language": missing_language,
            "shows_with_language_but_without_valid_rating": invalid_rating
        }