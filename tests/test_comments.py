"""
Comment Tests - SCRUM-16
"""
import pytest

class TestThreadedComments:
    """SCRUM-16: Threaded comment system"""
    
    def test_create_top_level_comment(self, client, auth_headers):
        response = client.post("/api/comments/", 
            headers=auth_headers,
            json={"content": "Great article!", "article_id": 1})
        assert response.status_code == 200
        assert response.json()["parent_id"] is None
    
    def test_max_nesting_depth_3(self, client, auth_headers):
        """SCRUM-16: Limit replies to 3 levels"""
        # Create 3 levels of nesting
        c1 = client.post("/api/comments/", headers=auth_headers,
            json={"content": "L1", "article_id": 1}).json()
        c2 = client.post("/api/comments/", headers=auth_headers,
            json={"content": "L2", "article_id": 1, "parent_id": c1["id"]}).json()
        c3 = client.post("/api/comments/", headers=auth_headers,
            json={"content": "L3", "article_id": 1, "parent_id": c2["id"]}).json()
        
        # Level 4 should fail
        r4 = client.post("/api/comments/", headers=auth_headers,
            json={"content": "L4", "article_id": 1, "parent_id": c3["id"]})
        assert r4.status_code == 400
