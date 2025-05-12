import pytest
from src.recommendation_engine import RecommendationEngine

@pytest.fixture
def setup_engine():
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
    return engine

def test_content_based_recommendation(setup_engine):
    recs = setup_engine.generate_recommendations('u1', algorithm='content_based')
    assert isinstance(recs, list)
    assert len(recs) > 0
    assert all(hasattr(r, 'title') for r in recs)

def test_additional_user_and_collaborative_recommendation(setup_engine):
    engine = setup_engine
    u2 = engine.add_user('u2', 'User Two')
    engine.users['u2'].update_preferences({'Action': 0.8})
    engine.users['u2'].add_viewing_record('c1', 7000, 1.0)
    engine.users['u2'].add_viewing_record('c2', 7000, 1.0)
    engine.content['c1'].ratings['u2'] = 5
    engine.content['c2'].ratings['u2'] = 4
    recs = engine.generate_recommendations('u1', algorithm='collaborative')
    assert len(recs) > 0

def test_hybrid_recommendation(setup_engine):
    recs = setup_engine.generate_recommendations('u1', algorithm='hybrid')
    assert isinstance(recs, list)
    assert len(recs) > 0
