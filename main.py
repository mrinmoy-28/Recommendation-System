#!/usr/bin/env python3
"""
Recommendation System - Main Module
This module provides a command-line interface for interacting with the recommendation engine.
"""

import os
import sys
import argparse
import json
from datetime import datetime, timedelta
import random

# Add the current directory to the Python path if needed
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Import recommendation system components
from src.recommendation_engine import RecommendationEngine
from src.content_metadata import Content
from src.user_profile import UserProfile
from src.utils import load_json_data, save_json_data

# Sample data for initialization
SAMPLE_GENRES = [
    "Action", "Adventure", "Animation", "Comedy", "Crime", 
    "Documentary", "Drama", "Fantasy", "Horror", "Mystery",
    "Romance", "Sci-Fi", "Thriller", "Western"
]

SAMPLE_TAGS = [
    "violent", "funny", "suspenseful", "thought-provoking", "heartwarming",
    "inspirational", "dark", "uplifting", "scary", "educational",
    "family-friendly", "epic", "dystopian", "biographical", "nostalgic"
]

SAMPLE_CONTENT_TYPES = ["movie", "series", "documentary", "short"]

class RecommendationSystem:
    """Main class that integrates all components of the recommendation system"""
    
    def __init__(self, data_dir="data"):
        """Initialize the recommendation system
        
        Args:
            data_dir (str): Directory for storing data files
        """
        self.data_dir = data_dir
        self.engine = RecommendationEngine()
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # File paths for persistence
        self.users_file = os.path.join(data_dir, "users.json")
        self.content_file = os.path.join(data_dir, "content.json")
        
    def load_data(self):
        """Load users and content data from files"""
        print("Loading data...")
        
        # Load users
        users_data = load_json_data(self.users_file)
        for user_id, user_data in users_data.items():
            user = self.engine.add_user(user_id, user_data.get("username"))
            
            # Load preferences
            if "preferences" in user_data:
                user.preferences = user_data["preferences"]
                
            # Load viewing history
            if "viewing_history" in user_data:
                for record in user_data["viewing_history"]:
                    # Convert timestamp string back to datetime if it exists
                    if "timestamp" in record:
                        # Timestamps are saved as strings, convert back to datetime
                        try:
                            record["timestamp"] = datetime.fromisoformat(record["timestamp"])
                        except (ValueError, TypeError):
                            record["timestamp"] = datetime.now()
                    user.viewing_history.append(record)
        
        # Load content
        content_data = load_json_data(self.content_file)
        for content_id, content_info in content_data.items():
            content = self.engine.add_content(
                content_id, 
                content_info.get("title", "Untitled"),
                content_info.get("content_type", "movie")
            )
            
            # Convert release_date string back to datetime if it exists
            if "release_date" in content_info and content_info["release_date"]:
                try:
                    content_info["release_date"] = datetime.fromisoformat(content_info["release_date"])
                except (ValueError, TypeError):
                    content_info["release_date"] = None
            
            # Update all content metadata
            content.update_metadata(content_info)
            
        print(f"Loaded {len(self.engine.users)} users and {len(self.engine.content_database)} content items")
        
    def save_data(self):
        """Save users and content data to files"""
        print("Saving data...")
        
        # Save users
        users_data = {}
        for user_id, user in self.engine.users.items():
            # Need to convert viewing history to be JSON serializable
            serializable_history = []
            for record in user.viewing_history:
                record_copy = record.copy()
                # Convert datetime to string if present
                if "timestamp" in record_copy:
                    record_copy["timestamp"] = record_copy["timestamp"].isoformat()
                serializable_history.append(record_copy)
                
            users_data[user_id] = {
                "username": user.username,
                "preferences": user.preferences,
                "viewing_history": serializable_history
            }
        
        save_json_data(users_data, self.users_file)
        
        # Save content
        content_data = {}
        for content_id, content in self.engine.content_database.items():
            # Convert content object to dictionary for JSON serialization
            content_dict = {
                "content_id": content.content_id,
                "title": content.title,
                "content_type": content.content_type,
                "description": content.description,
                "genres": content.genres,
                "tags": content.tags,
                "popularity_score": content.popularity_score,
                "ratings": content.ratings
            }
            
            # Handle release_date if it exists
            if content.release_date:
                content_dict["release_date"] = content.release_date.isoformat()
                
            content_data[content_id] = content_dict
            
        save_json_data(content_data, self.content_file)
        
        print("Data saved successfully")
        
    def generate_sample_data(self, num_users=20, num_content=100):
        """Generate sample data for testing
        
        Args:
            num_users (int): Number of users to generate
            num_content (int): Number of content items to generate
        """
        print(f"Generating sample data: {num_users} users, {num_content} content items")
        
        # Generate sample content
        for i in range(1, num_content + 1):
            content_id = f"c{i}"
            title = f"Sample Content {i}"
            content_type = random.choice(SAMPLE_CONTENT_TYPES)
            
            content = self.engine.add_content(content_id, title, content_type)
            
            # Add random metadata
            content.description = f"This is a sample {content_type} about various themes."
            content.genres = random.sample(SAMPLE_GENRES, random.randint(1, 3))
            content.tags = random.sample(SAMPLE_TAGS, random.randint(2, 5))
            
            # Random release date between 1980 and 2023
            year = random.randint(1980, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # Simplified to avoid month length issues
            content.release_date = datetime(year, month, day)
            
            # Duration between 20 and 180 minutes
            content.duration = random.randint(20, 180)
            
            # Random popularity score
            content.popularity_score = random.uniform(0, 10)
        
        # Generate sample users
        for i in range(1, num_users + 1):
            user_id = f"u{i}"
            username = f"User {i}"
            
            user = self.engine.add_user(user_id, username)
            
            # Add random genre preferences
            preferences = {}
            for _ in range(random.randint(2, 5)):
                genre = random.choice(SAMPLE_GENRES)
                preferences[genre] = random.uniform(0.3, 1.0)
            user.update_preferences(preferences)
            
            # Add random viewing history
            num_views = random.randint(5, 20)
            content_ids = list(self.engine.content_database.keys())
            
            for _ in range(num_views):
                content_id = random.choice(content_ids)
                watch_duration = random.randint(60, 7200)  # 1 minute to 2 hours
                completion = random.uniform(0.1, 1.0)
                
                # Add viewing record with a random timestamp in the past 30 days
                user.add_viewing_record(
                    content_id,
                    watch_duration,
                    completion
                )
                
                # Add random rating
                content = self.engine.content_database[content_id]
                if random.random() > 0.3:  # 70% chance of rating
                    content.ratings[user_id] = random.randint(1, 5)
        
        print("Sample data generated successfully")
    
    def get_recommendations(self, user_id, algorithm="hybrid", limit=10):
        """Get recommendations for a user
        
        Args:
            user_id (str): User ID
            algorithm (str): Recommendation algorithm to use
            limit (int): Maximum number of recommendations
            
        Returns:
            list: List of recommended content items
        """
        if user_id not in self.engine.users:
            print(f"User {user_id} not found.")
            return []
            
        print(f"Generating {algorithm} recommendations for user {user_id}...")
        recommendations = self.engine.generate_recommendations(
            user_id, algorithm=algorithm, limit=limit
        )
        
        return recommendations
        
    def display_recommendations(self, recommendations):
        """Display recommendations in a formatted way
        
        Args:
            recommendations (list): List of recommended Content objects
        """
        if not recommendations:
            print("No recommendations available.")
            return
            
        print(f"\nTop {len(recommendations)} Recommendations:")
        print("=" * 50)
        
        for i, content in enumerate(recommendations, 1):
            print(f"{i}. {content.title} ({content.content_type})")
            print(f"   Genres: {', '.join(content.genres)}")
            if content.release_date:
                print(f"   Released: {content.release_date.year}")
            print(f"   Rating: {content.get_average_rating():.1f}/5.0")
            print(f"   Popularity: {content.popularity_score:.1f}/10.0")
            print("-" * 50)
    
    def get_user_stats(self, user_id):
        """Get statistics about a user's viewing habits
        
        Args:
            user_id (str): User ID
            
        Returns:
            dict: User statistics
        """
        if user_id not in self.engine.users:
            print(f"User {user_id} not found.")
            return {}
            
        user = self.engine.users[user_id]
        
        # Calculate total watch time
        total_watch_time = sum(record["watch_duration"] for record in user.viewing_history)
        
        # Count content types watched
        content_types = {}
        for record in user.viewing_history:
            content_id = record["content_id"]
            if content_id in self.engine.content_database:
                content = self.engine.content_database[content_id]
                content_type = content.content_type
                content_types[content_type] = content_types.get(content_type, 0) + 1
        
        # Get favorite genres
        favorite_genres = user.get_favorite_genres(5)
        
        return {
            "user_id": user_id,
            "username": user.username,
            "total_watch_time": total_watch_time,
            "total_items_watched": len(user.viewing_history),
            "content_types": content_types,
            "favorite_genres": favorite_genres
        }
    
    def display_user_stats(self, stats):
        """Display user statistics in a formatted way
        
        Args:
            stats (dict): User statistics
        """
        if not stats:
            return
            
        print("\nUser Statistics:")
        print("=" * 50)
        print(f"User: {stats['username']} ({stats['user_id']})")
        print(f"Total items watched: {stats['total_items_watched']}")
        
        # Format watch time
        hours = stats['total_watch_time'] // 3600
        minutes = (stats['total_watch_time'] % 3600) // 60
        print(f"Total watch time: {hours} hours, {minutes} minutes")
        
        # Display content types
        print("\nContent Types Watched:")
        for content_type, count in stats['content_types'].items():
            print(f"- {content_type.capitalize()}: {count}")
        
        # Display favorite genres
        print("\nFavorite Genres:")
        for genre, score in stats['favorite_genres']:
            print(f"- {genre}: {score:.2f}")
            
        print("=" * 50)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Recommendation System CLI")
    
    # User options
    user_group = parser.add_argument_group("User Options")
    user_group.add_argument("--user", type=str, help="User ID for recommendations")
    user_group.add_argument("--stats", action="store_true", help="Show user statistics")
    
    # Recommendation options
    rec_group = parser.add_argument_group("Recommendation Options")
    rec_group.add_argument(
        "--algorithm", 
        type=str, 
        choices=["content_based", "collaborative", "hybrid", "popular"],
        default="hybrid", 
        help="Recommendation algorithm to use"
    )
    rec_group.add_argument(
        "--limit", 
        type=int, 
        default=5,
        help="Number of recommendations to show"
    )
    
    # Data options
    data_group = parser.add_argument_group("Data Options")
    data_group.add_argument(
        "--generate", 
        action="store_true",
        help="Generate new sample data"
    )
    data_group.add_argument(
        "--users", 
        type=int, 
        default=20,
        help="Number of sample users to generate"
    )
    data_group.add_argument(
        "--content", 
        type=int, 
        default=100,
        help="Number of sample content items to generate"
    )
    data_group.add_argument(
        "--no-save", 
        action="store_true",
        help="Don't save data after execution"
    )
    
    return parser.parse_args()


def main():
    """Main function"""
    args = parse_arguments()
    
    # Initialize recommendation system
    system = RecommendationSystem()
    
    try:
        # Load existing data
        system.load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        print("Starting with empty data")
    
    # Generate sample data if requested
    if args.generate:
        system.generate_sample_data(args.users, args.content)
    
    # Handle user statistics
    if args.stats and args.user:
        stats = system.get_user_stats(args.user)
        system.display_user_stats(stats)
    
    # Handle recommendations
    if args.user:
        recommendations = system.get_recommendations(
            args.user, 
            algorithm=args.algorithm,
            limit=args.limit
        )
        system.display_recommendations(recommendations)
    elif not args.stats and not args.generate:
        # No specific task, show recommendations for a random user
        if system.engine.users:
            random_user_id = random.choice(list(system.engine.users.keys()))
            print(f"Showing recommendations for random user: {random_user_id}")
            recommendations = system.get_recommendations(
                random_user_id,
                algorithm=args.algorithm,
                limit=args.limit
            )
            system.display_recommendations(recommendations)
        else:
            print("No users available. Use --generate to create sample data.")
    
    # Save data unless explicitly disabled
    if not args.no_save:
        system.save_data()


if __name__ == "__main__":
    main()