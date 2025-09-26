#!/bin/bash

# I generated this script with sonnet.

# API Testing Script for Ekubo Backend
# Make sure the server is running: python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

BASE_URL="http://localhost:8000"
API_BASE="$BASE_URL/api"

echo "🚀 Testing Ekubo API Endpoints"
echo "================================"

# Test 1: Health Check - Get API Documentation
echo "📋 Test 1: API Documentation"
curl -s "$BASE_URL/docs" | grep -q "Swagger" && echo "✅ API docs accessible" || echo "❌ API docs not accessible"

# Test 2: Legacy Songs API
echo ""
echo "🎵 Test 2: Legacy Songs API"
echo "Searching for lyrics..."
curl -s -X GET "$BASE_URL/songs/lyrics?q=きみにとどけ" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 3: Spotify Search
echo ""
echo "🎧 Test 3: Spotify Search"
echo "Searching for Spotify tracks..."
curl -s -X GET "$BASE_URL/songs/spotify-tracks?track_name=きみにとどけ&artist_name=谷澤智文&track_limit=3" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 4: New Songs API
echo ""
echo "🎼 Test 4: New Songs API"
echo "Getting all songs..."
curl -s -X GET "$API_BASE/songs/" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 5: Create a Song
echo ""
echo "➕ Test 5: Create a Song"
echo "Creating a new song..."
curl -s -X POST "$API_BASE/songs/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Song",
    "artist": "Test Artist",
    "album": "Test Album",
    "duration": 180,
    "spotify_id": "test123"
  }' | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 6: Lyrics API
echo ""
echo "📝 Test 6: Lyrics API"
echo "Getting all lyrics..."
curl -s -X GET "$API_BASE/lyrics/" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 7: Create Lyrics
echo ""
echo "➕ Test 7: Create Lyrics"
echo "Creating new lyrics..."
curl -s -X POST "$API_BASE/lyrics/" \
  -H "Content-Type: application/json" \
  -d '{
    "synced_lyrics": "[00:12.34]君に届け 君に届け\n[00:15.67]心の声が 聞こえるかな"
  }' | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 8: Matched Songs API
echo ""
echo "🔗 Test 8: Matched Songs API"
echo "Getting all matched songs..."
curl -s -X GET "$API_BASE/matched/" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 9: User Library API
echo ""
echo "📚 Test 9: User Library API"
echo "Getting user library (user_id=1)..."
curl -s -X GET "$API_BASE/library/1" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

# Test 10: Authentication
echo ""
echo "🔐 Test 10: Authentication"
echo "Testing signup..."
curl -s -X POST "$BASE_URL/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123"
  }' | jq '.' 2>/dev/null || echo "Response received (not JSON)"

echo ""
echo "🎯 Test 11: Search Existing Matches"
echo "Searching for existing matches..."
curl -s -X GET "$API_BASE/matched/search/existing" | jq '.' 2>/dev/null || echo "Response received (not JSON)"

echo ""
echo "✅ API Testing Complete!"
echo "================================"
echo "📖 View full API documentation at: $BASE_URL/docs"
echo "🔧 View OpenAPI spec at: $BASE_URL/openapi.json"


