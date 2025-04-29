from datetime import datetime

class UserProfile:
    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username
        self.preferences = {}  # genre -> preference score
        self.viewing_history = []
        
    def update_preferences(self, preferences):
        """Update user genre preferences
        
        Args:
            preferences (dict): Dictionary mapping genre to preference score (0-1)
        """
        for genre, score in preferences.items():
            if 0 <= score <= 1:
                self.preferences[genre] = score
            else:
                raise ValueError(f"Preference score must be between 0 and 1, got {score}")
    
    def add_viewing_record(self, content_id, watch_duration, completion_percentage):
        """Add a viewing record to user history
        
        Args:
            content_id (str): ID of the watched content
            watch_duration (int): Duration watched in seconds
            completion_percentage (float): Percentage of content watched (0-1)
        """
        record = {
            "content_id": content_id,
            "watch_duration": watch_duration,
            "completion_percentage": completion_percentage,
            "timestamp": datetime.now()
        }
        self.viewing_history.append(record)
    
    def get_favorite_genres(self, top_n=3):
        """Get user's top preferred genres
        
        Args:
            top_n (int): Number of top genres to return
            
        Returns:
            list: List of (genre, score) tuples sorted by preference
        """
        return sorted(self.preferences.items(), key=lambda x: x[1], reverse=True)[:top_n]