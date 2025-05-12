import cProfile
import pstats
from src.recommendation_engine import RecommendationEngine

def run_workload():
    engine = RecommendationEngine()

    # Add sample content
    c1 = engine.add_content('c1', 'Avengers', 'movie')
    c1.genres = ['Action', 'Adventure']
    c1.tags = ['hero', 'team']
    c1.popularity_score = 9.5

    c2 = engine.add_content('c2', 'Inception', 'movie')
    c2.genres = ['Sci-Fi', 'Thriller']
    c2.tags = ['dream', 'mind']
    c2.popularity_score = 8.7

    c3 = engine.add_content('c3', 'Friends', 'series')
    c3.genres = ['Comedy', 'Romance']
    c3.tags = ['sitcom', 'funny']
    c3.popularity_score = 8.2

    engine.add_user('u1', 'User One')
    engine.users['u1'].update_preferences({'Action': 0.9, 'Comedy': 0.5})
    engine.users['u1'].add_viewing_record('c1', 7000, 1.0)
    engine.users['u1'].add_viewing_record('c3', 1000, 0.3)
    c1.ratings['u1'] = 5
    c3.ratings['u1'] = 3

    # Generate recommendations
    for _ in range(100):  # simulate 100 recommendation requests
        engine.generate_recommendations('u1', algorithm='hybrid')

if __name__ == "__main__":
    cProfile.run('run_workload()', 'profile_output.prof')
