class TVShow:
    """Represents one TV show and cleans its data."""

    def __init__(self, data):
        # Clean the show's name
        name = data.get("name")
        self.name = name.strip() if isinstance(name, str) else ""

        # Clean genres and count invalid entries
        genres = data.get("genres")
        self.invalid_genre_entries = 0

        if isinstance(genres, list):
            self.genres = set()

            for genre in genres:
                if isinstance(genre, str) and genre.strip():
                    self.genres.add(genre.strip())
                else:
                    self.invalid_genre_entries += 1
        else:
            self.genres = set()

        # Clean language
        language = data.get("language")

        if isinstance(language, str) and language.strip():
            self.language = language.strip()
        else:
            self.language = None

        # Clean rating
        rating_data = data.get("rating")

        if isinstance(rating_data, dict):
            rating = rating_data.get("average")
        else:
            rating = None

        if (
            isinstance(rating, bool)
            or not isinstance(rating, (int, float))
            or not 0 <= rating <= 10
        ):
            self.rating = None
        else:
            self.rating = rating

    def __str__(self):
        return self.name