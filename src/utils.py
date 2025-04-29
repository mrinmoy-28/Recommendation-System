import numpy as np
import json
import os

def calculate_content_similarity(content1, content2):
    """Calculate similarity between two content items
    
    Args:
        content1 (Content): First content item
        content2 (Content): Second content item
        
    Returns:
        float: Similarity score between 0 and 1
    """
    # Get feature vectors
    features1 = content1.to_feature_vector()
    features2 = content2.to_feature_vector()
    
    # Calculate genre similarity
    genre_sim = calculate_jaccard_similarity(features1["genres"], features2["genres"])
    
    # Calculate tag similarity
    tag_sim = calculate_jaccard_similarity(features1["tags"], features2["tags"])
    
    # Calculate rating and popularity similarity
    rating_diff = abs(features1["avg_rating"] - features2["avg_rating"]) / 5.0  # Normalize to 0-1
    pop_diff = abs(features1["popularity"] - features2["popularity"])
    
    # Calculate type similarity (1 if same type, 0 otherwise)
    type_sim = 1.0 if features1["content_type"] == features2["content_type"] else 0.0
    
    # Weighted combination
    sim_score = (0.4 * genre_sim + 0.3 * tag_sim + 0.1 * (1 - rating_diff) + 
                0.1 * (1 - pop_diff) + 0.1 * type_sim)
    
    return sim_score

def calculate_jaccard_similarity(set1, set2):
    """Calculate Jaccard similarity between two sets
    
    Args:
        set1 (list): First set of items
        set2 (list): Second set of items
        
    Returns:
        float: Jaccard similarity coefficient
    """
    set1 = set(set1)
    set2 = set(set2)
    
    if not set1 and not set2:
        return 1.0  # Both empty means perfect similarity
        
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    
    return intersection / union if union > 0 else 0.0

def load_json_data(filepath):
    """Load data from JSON file
    
    Args:
        filepath (str): Path to JSON file
        
    Returns:
        dict: Loaded JSON data
    """
    if not os.path.exists(filepath):
        return {}
        
    with open(filepath, 'r') as f:
        return json.load(f)

def save_json_data(data, filepath):
    """Save data to JSON file
    
    Args:
        data (dict): Data to save
        filepath (str): Path to JSON file
    """
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)