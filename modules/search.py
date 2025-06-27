import numpy as np
from datetime import datetime
from config import Config
from utils.logger import logger
import random

class RLSearchEnhancer:
    def __init__(self, version_db):
        self.db = version_db
        self.learning_rate = Config.SEARCH_LEARNING_RATE
        self.memory = []
        self.weights = {
            "content_relevance": 1.0,
            "version_recency": 0.8,
            "human_rating": 1.2,
            "author_trust": 0.9
        }

    def search(self, query, chapter_name=None, limit=5):
        """Enhanced search with RL adjustments"""
        try:
            results = self.db.search_versions(query, chapter_name, limit*2)
            if not results:
                return []
                
            scored_results = [
                (self._calculate_score(result), result)
                for result in results
            ]
            scored_results.sort(reverse=True, key=lambda x: x[0])
            
            final_results = [r[1] for r in scored_results[:limit]]
            self._store_in_memory(query, final_results)
            return final_results
            
        except Exception as e:
            logger.error(f"RL search failed: {str(e)}")
            return []
    
    def _calculate_score(self, result):
        """Calculate weighted score for a result"""
        metadata = result.get("metadata", {})
        
        # Base score from embedding distance (inverted)
        base_score = 1 - result.get("distance", 1)
        
        # Apply weights
        weighted_score = base_score * self.weights["content_relevance"]
        
        # Version recency (newer is better)
        timestamp = metadata.get("timestamp", "")
        if timestamp:
            days_old = (datetime.now() - datetime.fromisoformat(timestamp)).days
            recency_factor = max(0, 1 - (days_old / 365))
            weighted_score += recency_factor * self.weights["version_recency"]
        
        # Human rating if available
        if "human_rating" in metadata:
            weighted_score += metadata["human_rating"] * self.weights["human_rating"]
        
        # Author trust factor
        if metadata.get("author") == "human_editor":
            weighted_score *= self.weights["author_trust"]
            
        return weighted_score
    
    def _store_in_memory(self, query, results):
        """Store search session in memory for learning"""
        if len(self.memory) >= Config.SEARCH_MEMORY_SIZE:
            self.memory.pop(0)
            
        self.memory.append({
            "query": query,
            "results": results,
            "selected": None  # To be filled when user selects a result
        })
    
    def update_weights(self, selected_result):
        """Update weights based on user selection"""
        try:
            # Find the search session where this result was shown
            for session in self.memory:
                if selected_result in session["results"]:
                    session["selected"] = selected_result
                    
                    # Get features of selected result
                    selected_features = self._extract_features(selected_result)
                    
                    # Update weights
                    for feature, value in selected_features.items():
                        if feature in self.weights:
                            self.weights[feature] += self.learning_rate * value
                    
                    break
                    
            # Normalize weights
            total = sum(self.weights.values())
            self.weights = {k: v/total for k, v in self.weights.items()}
            
        except Exception as e:
            logger.error(f"Weight update failed: {str(e)}")
    
    def _extract_features(self, result):
        """Extract features from a result for RL"""
        metadata = result.get("metadata", {})
        
        return {
            "content_relevance": 1 - result.get("distance", 1),
            "version_recency": 1 - min(1, (datetime.now() - datetime.fromisoformat(
                metadata.get("timestamp", datetime.now().isoformat())
            )).days / 365),
            "human_rating": metadata.get("human_rating", 0.5),
            "author_trust": 1 if metadata.get("author") == "human_editor" else 0.5
        }