"""
Authentication Tests - SCRUM-11
"""
import pytest
from fastapi.testclient import TestClient

class TestJWTAuth:
    """SCRUM-11: JWT Authentication"""
    
    def test_login_returns_tokens(self, client):
        response = client.post("/api/auth/login", json={
            "email": "test@dailytribune.com",
            "password": "testpass123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()
    
    def test_refresh_rotates_tokens(self, client, refresh_token):
        """Old refresh token should be invalidated after use"""
        # Use refresh token
        r1 = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        assert r1.status_code == 200
        
        # Try using old token again - should fail
        r2 = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        assert r2.status_code == 401
