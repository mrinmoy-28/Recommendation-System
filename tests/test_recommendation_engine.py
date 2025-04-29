#!/usr/bin/env python3
"""
Test script for the recommendation system.
This script demonstrates how to use the recommendation system in Python code.
"""

from src.recommendation_engine import RecommendationEngine
from src.content_metadata import Content
from src.user_profile import UserProfile

def test_recommendation_system():
    """
    Test the recommendation system with a small example.
    """
    # Initialize recommendation engine
    engine = RecommendationEngine()
    
    # Create some sample content
    avengers = engine.add_content('c1', 'Avengers: Endgame', 'movie')
    avengers.genres = ['Action', 'Adventure', 'Sci-Fi']
    avengers.tags = ['superhero', 'epic', 'team']
    avengers.popularity_score = 9.5
    
    inception = engine.add_content('c2', 'Inception', 'movie')
    inception.genres = ['Sci-Fi', 'Thriller', 'Action']
    inception.tags = ['mind-bending', 'dream', 'heist']
    inception.popularity_score = 8.7
    
    friends = engine.add_content('c3', 'Friends', 'series')
    friends.genres = ['Comedy', 'Romance']
    friends.tags = ['funny', 'sitcom', 'friendship']
    friends.popularity_score = 8.2
    
    breaking_bad = engine.add_content('c4', 'Breaking Bad', 'series')
    breaking_bad.genres = ['Drama', 'Crime', 'Thriller']
    breaking_bad.tags = ['dark', 'drug', 'suspenseful']
    breaking_bad.popularity_score = 9.8
    
    nature = engine.add_content('c5', 'Planet Earth', 'documentary')
    nature.genres = ['Documentary', 'Nature']
    nature.tags = ['educational', 'animals', 'nature']
    nature.popularity_score = 8.5
    
    # Create a test user
    user = engine.add_user('u1', 'Test User')
    
    # Add some genre preferences
    preferences = {
        'Action': 0.8,
        'Sci-Fi': 0.9,
        'Comedy': 0.3,
        'Drama': 0.5
    }
    user.update_preferences(preferences)
    
    # Add some viewing history
    user.add_viewing_record('c1', 7200, 1.0)  # Watched Avengers completely
    user.add_viewing_record('c3', 1200, 0.4)  # Watched part of Friends
    
    # Add some ratings
    avengers.ratings['u1'] = 5  # Rated Avengers 5/5
    friends.ratings['u1'] = 3   # Rated Friends 3/5
    
    # Generate recommendations using different algorithms
    print("\n=== Content-Based Recommendations ===")
    content_recs = engine.generate_recommendations('u1', algorithm='content_based', limit=3)
    for i, rec in enumerate(content_recs, 1):
        print(f"{i}. {rec.title} ({', '.join(rec.genres)})")
    
    print("\n=== Collaborative Recommendations ===")
    # For collaborative filtering, we need more users, so let's add another one
    user2 = engine.add_user('u2', 'Similar User')
    user2.update_preferences({
        'Action': 0.7,
        'Sci-Fi': 0.8,
        'Drama': 0.6
    })
    user2.add_viewing_record('c1', 7000, 0.95)  # Also watched Avengers
    user2.add_viewing_record('c2', 6000, 0.9)   # Watched Inception
    user2.add_viewing_record('c4', 12000, 1.0)  # Watched Breaking Bad
    
    avengers.ratings['u2'] = 5  # Also rated Avengers 5/5
    inception.ratings['u2'] = 5 # Rated Inception 5/5
    breaking_bad.ratings['u2'] = 4 # Rated Breaking Bad 4/5
    
    collab_recs = engine.generate_recommendations('u1', algorithm='collaborative', limit=3)
    for i, rec in enumerate(collab_recs, 1):
        print(f"{i}. {rec.title} ({', '.join(rec.genres)})")
    
    print("\n=== Hybrid Recommendations ===")
    hybrid_recs = engine.generate_recommendations('u1', algorithm='hybrid', limit=3)
    for i, rec in enumerate(hybrid_recs, 1):
        print(f"{i}. {rec.title} ({', '.join(rec.genres)})")

if __name__ == "__main__":
    test_recommendation_system()