import numpy as np
from collections import defaultdict
from src.user_profile import UserProfile
from src.content_metadata import Content
from src.utils import calculate_content_similarity

class RecommendationEngine:
    """
    AI-powered recommendation engine for streaming content.
    
    This engine uses multiple recommendation strategies:
    1. Content-based filtering: Recommends items similar to what the user has liked
    2. Collaborative filtering: Recommends items liked by similar users
    3. Hybrid approach: Combines both methods for better recommendations
    """
    
    def __init__(self):
        """Initialize the recommendation engine"""
        self.users = {}  # user_id -> UserProfile
        self.content_database = {}  # content_id -> Content
        self.content_similarity_cache = {}  # (content_id1, content_id2) -> similarity_score
        self.user_similarity_cache = {}  # (user_id1, user_id2) -> similarity_score
        
    def add_user(self, user_id, username=None):
        """Add a new user to the system
        
        Args:
            user_id (str): Unique user identifier
            username (str, optional): User's name
            
        Returns:
            UserProfile: The newly created user profile
        """
        if user_id in self.users:
            return self.users[user_id]
            
        user = UserProfile(user_id, username)
        self.users[user_id] = user
        return user
        
    def add_content(self, content_id, title, content_type):
        """Add new content to the database
        
        Args:
            content_id (str): Unique content identifier
            title (str): Content title
            content_type (str): Type of content (movie, series, etc.)
            
        Returns:
            Content: The newly created content object
        """
        if content_id in self.content_database:
            return self.content_database[content_id]
            
        content = Content(content_id, title, content_type)
        self.content_database[content_id] = content
        return content
        
    def update_user_preferences(self, user_id, preferences):
        """Update a user's genre preferences
        
        Args:
            user_id (str): User identifier
            preferences (dict): Dictionary of genre -> preference score (0-1)
        """
        if user_id not in self.users:
            self.add_user(user_id)
            
        self.users[user_id].update_preferences(preferences)
        
        # Clear cached user similarities since preferences changed
        self._clear_user_similarity_cache(user_id)
        
    def add_viewing_record(self, user_id, content_id, watch_duration, completion_percentage):
        """Add a viewing record to user history
        
        Args:
            user_id (str): User identifier
            content_id (str): Content identifier
            watch_duration (int): Duration watched in seconds
            completion_percentage (float): Percentage of content watched (0-1)
        """
        if user_id not in self.users:
            self.add_user(user_id)
            
        self.users[user_id].add_viewing_record(content_id, watch_duration, completion_percentage)
        
        # Clear cached user similarities since viewing history changed
        self._clear_user_similarity_cache(user_id)
        
    def _clear_user_similarity_cache(self, user_id):
        """Clear user similarity cache entries for a specific user
        
        Args:
            user_id (str): User identifier
        """
        keys_to_clear = []
        for key in self.user_similarity_cache:
            if user_id in key:
                keys_to_clear.append(key)
                
        for key in keys_to_clear:
            del self.user_similarity_cache[key]
    
    def _get_content_similarity(self, content_id1, content_id2):
        """Get similarity between two content items, using cache if available
        
        Args:
            content_id1 (str): First content identifier
            content_id2 (str): Second content identifier
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Check if items exist
        if content_id1 not in self.content_database or content_id2 not in self.content_database:
            return 0.0
            
        # Create a consistent key for the cache (smaller id first)
        if content_id1 > content_id2:
            content_id1, content_id2 = content_id2, content_id1
            
        cache_key = (content_id1, content_id2)
        
        # Return cached value if available
        if cache_key in self.content_similarity_cache:
            return self.content_similarity_cache[cache_key]
            
        # Calculate similarity
        content1 = self.content_database[content_id1]
        content2 = self.content_database[content_id2]
        similarity = calculate_content_similarity(content1, content2)
        
        # Cache the result
        self.content_similarity_cache[cache_key] = similarity
        
        return similarity
    
    def _calculate_user_similarity(self, user_id1, user_id2):
        """Calculate similarity between two users based on preferences and history
        
        Args:
            user_id1 (str): First user identifier
            user_id2 (str): Second user identifier
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Check if users exist
        if user_id1 not in self.users or user_id2 not in self.users:
            return 0.0
            
        # Create a consistent key for the cache (smaller id first)
        if user_id1 > user_id2:
            user_id1, user_id2 = user_id2, user_id1
            
        cache_key = (user_id1, user_id2)
        
        # Return cached value if available
        if cache_key in self.user_similarity_cache:
            return self.user_similarity_cache[cache_key]
            
        user1 = self.users[user_id1]
        user2 = self.users[user_id2]
        
        # Calculate preference similarity
        preference_sim = self._calculate_preference_similarity(user1, user2)
        
        # Calculate viewing history similarity
        history_sim = self._calculate_history_similarity(user1, user2)
        
        # Weighted combination
        similarity = 0.6 * preference_sim + 0.4 * history_sim
        
        # Cache the result
        self.user_similarity_cache[cache_key] = similarity
        
        return similarity
    
    def _calculate_preference_similarity(self, user1, user2):
        """Calculate similarity between users' genre preferences
        
        Args:
            user1 (UserProfile): First user profile
            user2 (UserProfile): Second user profile
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Get all genres from both users
        all_genres = set(user1.preferences.keys()) | set(user2.preferences.keys())
        
        if not all_genres:
            return 0.0  # No preferences to compare
            
        # Calculate cosine similarity
        sum_products = 0.0
        sum_squares1 = 0.0
        sum_squares2 = 0.0
        
        for genre in all_genres:
            score1 = user1.preferences.get(genre, 0.0)
            score2 = user2.preferences.get(genre, 0.0)
            
            sum_products += score1 * score2
            sum_squares1 += score1 * score1
            sum_squares2 += score2 * score2
            
        # Avoid division by zero
        if sum_squares1 == 0 or sum_squares2 == 0:
            return 0.0
            
        return sum_products / (np.sqrt(sum_squares1) * np.sqrt(sum_squares2))
    
    def _calculate_history_similarity(self, user1, user2):
        """Calculate similarity between users' viewing histories
        
        Args:
            user1 (UserProfile): First user profile
            user2 (UserProfile): Second user profile
            
        Returns:
            float: Similarity score between 0 and 1
        """
        # Extract content IDs from viewing histories
        history1 = {record["content_id"] for record in user1.viewing_history}
        history2 = {record["content_id"] for record in user2.viewing_history}
        
        if not history1 or not history2:
            return 0.0  # No history to compare
            
        # Calculate Jaccard similarity
        intersection = len(history1 & history2)
        union = len(history1 | history2)
        
        return intersection / union
    
    def content_based_filtering(self, user_id, limit=10):
        """Generate recommendations based on content similarity to user preferences
        
        Args:
            user_id (str): User identifier
            limit (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended content IDs
        """
        if user_id not in self.users:
            return self.get_popular_content(limit)
            
        user = self.users[user_id]
        
        # Get content items the user has watched
        watched_content = {record["content_id"] for record in user.viewing_history}
        
        # Calculate content scores based on similarity to watched content
        content_scores = defaultdict(float)
        
        for watched_id in watched_content:
            # Skip if content is no longer in database
            if watched_id not in self.content_database:
                continue
                
            for candidate_id in self.content_database:
                # Skip already watched content
                if candidate_id in watched_content:
                    continue
                    
                # Get similarity between watched and candidate content
                similarity = self._get_content_similarity(watched_id, candidate_id)
                
                # Find the viewing record for this content
                for record in user.viewing_history:
                    if record["content_id"] == watched_id:
                        # Weight by completion percentage - higher completion means stronger signal
                        weight = record["completion_percentage"]
                        content_scores[candidate_id] += similarity * weight
                        break
        
        # Sort by score
        recommendations = sorted(content_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N content IDs
        return [content_id for content_id, score in recommendations[:limit]]
    
    def collaborative_filtering(self, user_id, limit=10):
        """Generate recommendations based on similar users' preferences
        
        Args:
            user_id (str): User identifier
            limit (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended content IDs
        """
        if user_id not in self.users:
            return self.get_popular_content(limit)
            
        user = self.users[user_id]
        
        # Get content items the user has already watched
        watched_content = {record["content_id"] for record in user.viewing_history}
        
        # Calculate user similarities
        user_similarities = {}
        for other_id in self.users:
            if other_id != user_id:
                user_similarities[other_id] = self._calculate_user_similarity(user_id, other_id)
        
        # Sort users by similarity
        similar_users = sorted(user_similarities.items(), key=lambda x: x[1], reverse=True)
        
        # Take top 10 similar users
        top_similar_users = similar_users[:10]
        
        # Calculate content scores based on similar users' histories
        content_scores = defaultdict(float)
        
        for other_id, similarity in top_similar_users:
            other_user = self.users[other_id]
            
            for record in other_user.viewing_history:
                content_id = record["content_id"]
                
                # Skip already watched content
                if content_id in watched_content:
                    continue
                    
                # Skip if content is no longer in database
                if content_id not in self.content_database:
                    continue
                    
                # Weight by user similarity and completion percentage
                weight = similarity * record["completion_percentage"]
                content_scores[content_id] += weight
        
        # Sort by score
        recommendations = sorted(content_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N content IDs
        return [content_id for content_id, score in recommendations[:limit]]
    
    def hybrid_filtering(self, user_id, limit=10):
        """Combine content-based and collaborative filtering approaches
        
        Args:
            user_id (str): User identifier
            limit (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended content IDs
        """
        # Get recommendations from both methods
        content_recs = self.content_based_filtering(user_id, limit=limit)
        collab_recs = self.collaborative_filtering(user_id, limit=limit)
        
        # Combine recommendations with weights
        content_scores = {rec: 0.6 * (limit - i) for i, rec in enumerate(content_recs)}
        collab_scores = {rec: 0.4 * (limit - i) for i, rec in enumerate(collab_recs)}
        
        # Merge scores
        final_scores = defaultdict(float)
        for rec, score in content_scores.items():
            final_scores[rec] += score
        for rec, score in collab_scores.items():
            final_scores[rec] += score
        
        # Sort by final score
        recommendations = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return top N content IDs
        return [content_id for content_id, score in recommendations[:limit]]
    
    def get_popular_content(self, limit=10):
        """Get most popular content for cold start situations
        
        Args:
            limit (int): Maximum number of items to return
            
        Returns:
            list: List of popular content IDs
        """
        # Sort content by popularity score
        popular_content = sorted(
            self.content_database.items(),
            key=lambda x: x[1].popularity_score,
            reverse=True
        )
        
        # Return top N content IDs
        return [content_id for content_id, _ in popular_content[:limit]]
    
    def generate_recommendations(self, user_id, algorithm="hybrid", limit=10):
        """Generate recommendations using the specified algorithm
        
        Args:
            user_id (str): User identifier
            algorithm (str): One of 'content_based', 'collaborative', or 'hybrid'
            limit (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended content objects
        """
        # Map algorithm name to method
        algorithm_map = {
            "content_based": self.content_based_filtering,
            "collaborative": self.collaborative_filtering,
            "hybrid": self.hybrid_filtering
        }
        
        if algorithm not in algorithm_map:
            raise ValueError(f"Algorithm {algorithm} not supported. Use one of: {list(algorithm_map.keys())}")
        
        # Generate recommendation IDs using the selected algorithm
        recommendation_ids = algorithm_map[algorithm](user_id, limit)
        
        # Convert IDs to Content objects
        recommendations = [self.content_database[content_id] for content_id in recommendation_ids 
                          if content_id in self.content_database]
        
        return recommendations