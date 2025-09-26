# 🧪 Curl Test Examples for Ekubo API

Make sure the server is running first:
```bash
cd ekubo-backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Basic Health Checks

### 1. Check API Documentation
```bash
curl http://localhost:8000/docs
```

### 2. Get OpenAPI Spec
```bash
curl http://localhost:8000/openapi.json | jq '.'
```

## 🎵 Songs API Tests

### 3. Get All Songs
```bash
curl -X GET "http://localhost:8000/api/songs/" | jq '.'
```

### 4. Create a New Song
```bash
curl -X POST "http://localhost:8000/api/songs/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "君に届け",
    "artist": "谷澤智文",
    "album": "君に届け",
    "duration": 240,
    "spotify_id": "4dQJMakNxXhiwiVfIJqBGI"
  }' | jq '.'
```

### 5. Search Spotify Tracks
```bash
curl -X GET "http://localhost:8000/api/songs/search/spotify?track_name=君に届け&artist_name=谷澤智文&track_limit=3" | jq '.'
```

### 6. Search Lyrics (LRCLIB)
```bash
curl -X GET "http://localhost:8000/api/songs/search/lyrics?q=君に届け" | jq '.'
```

## 📝 Lyrics API Tests

### 7. Get All Lyrics
```bash
curl -X GET "http://localhost:8000/api/lyrics/" | jq '.'
```

### 8. Create New Lyrics
```bash
curl -X POST "http://localhost:8000/api/lyrics/" \
  -H "Content-Type: application/json" \
  -d '{
    "synced_lyrics": "[00:12.34]君に届け 君に届け 君に届け\n[00:15.67]心の声が 聞こえるかな\n[00:18.90]君に届け 君に届け 君に届け"
  }' | jq '.'
```

### 9. Get Lyrics with Lines (replace {lyrics_id} with actual ID)
```bash
curl -X GET "http://localhost:8000/api/lyrics/1" | jq '.'
```

## 🔗 Matched Songs API Tests

### 10. Get All Matched Songs
```bash
curl -X GET "http://localhost:8000/api/matched/" | jq '.'
```

### 11. Create Song-Lyrics Match
```bash
curl -X POST "http://localhost:8000/api/matched/" \
  -H "Content-Type: application/json" \
  -d '{
    "song_id": 1,
    "lyrics_id": 1,
    "created_by_user_id": 1
  }' | jq '.'
```

### 12. Search Existing Matches
```bash
curl -X GET "http://localhost:8000/api/matched/search/existing?song_id=1&lyrics_id=1" | jq '.'
```

## 📚 User Library API Tests

### 13. Get User Library
```bash
curl -X GET "http://localhost:8000/api/library/1" | jq '.'
```

### 14. Add Song to Library
```bash
curl -X POST "http://localhost:8000/api/library/1/add" \
  -H "Content-Type: application/json" \
  -d '{
    "matched_song_id": 1
  }' | jq '.'
```

### 15. Update Library Entry
```bash
curl -X PUT "http://localhost:8000/api/library/1/1" \
  -H "Content-Type: application/json" \
  -d '{
    "is_favorite": true,
    "practice_count": 5
  }' | jq '.'
```

## 🔐 Authentication Tests

### 16. User Signup
```bash
curl -X POST "http://localhost:8000/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpassword123"
  }' | jq '.'
```

### 17. User Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }' | jq '.'
```

## 🎯 Legacy API Tests

### 18. Legacy Lyrics Search
```bash
curl -X GET "http://localhost:8000/songs/lyrics?q=君に届け" | jq '.'
```

### 19. Legacy Spotify Search
```bash
curl -X GET "http://localhost:8000/songs/spotify-tracks?track_name=君に届け&artist_name=谷澤智文&track_limit=3" | jq '.'
```

## 🚀 Quick Test Script

Run the automated test script:
```bash
./test_api.sh
```

## 📖 Interactive Documentation

Visit these URLs in your browser:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Troubleshooting

If you get connection errors:
1. Make sure the server is running: `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000`
2. Check if port 8000 is available: `netstat -tulpn | grep 8000`
3. Try a different port: `python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001`

If you get database errors:
- The API will still work for testing, but database operations will fail
- Check your `.env` file and database connection
- The server will continue running even if database connection fails


