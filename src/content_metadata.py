class Content:
    def __init__(self, content_id, title, content_type):
        self.content_id = content_id
        self.title = title
        self.content_type = content_type  # movie, series, documentary, etc.
        self.description = ""
        self.genres = []
        self.release_date = None
        self.duration = None  # in minutes
        self.actors = []
        self.directors = []
        self.tags = []
        self.ratings = {}  # user_id -> rating
        self.popularity_score = 0.0
        
    def update_metadata(self, metadata_dict):
        """Update content metadata from dictionary
        
        Args:
            metadata_dict (dict): Dictionary with metadata fields
        """
        for key, value in metadata_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
    def get_average_rating(self):
        """Calculate average user rating
        
        Returns:
            float: Average rating or 0 if no ratings
        """
        if not self.ratings:
            return 0.0
        return sum(self.ratings.values()) / len(self.ratings)
    
    def to_feature_vector(self):
        """Convert content metadata to feature vector for similarity calculation
        
        Returns:
            dict: Feature vector representation
        """
        features = {
            "content_type": self.content_type,
            "genres": self.genres.copy(),
            "avg_rating": self.get_average_rating(),
            "popularity": self.popularity_score,
            "release_year": self.release_date.year if self.release_date else None,
            "tags": self.tags.copy()
        }
        return features