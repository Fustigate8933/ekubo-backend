"""
Supabase service for database operations using REST API.
"""
import os
from typing import Any, Dict, List, Optional
from httpx import AsyncClient
from fastapi import HTTPException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SupabaseService:
    """Service for interacting with Supabase database via REST API."""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Make a request to Supabase REST API."""
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        async with AsyncClient() as client:
            if method.upper() == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method.upper() == "POST":
                response = await client.post(url, headers=headers, json=data, params=params)
            elif method.upper() == "PUT":
                response = await client.put(url, headers=headers, json=data, params=params)
            elif method.upper() == "PATCH":
                response = await client.patch(url, headers=headers, json=data, params=params)
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=headers, params=params)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Supabase API error: {response.text}"
                )
            
            return response.json() if response.content else None
    
    async def get(self, table: str, record_id: int) -> Optional[Dict[str, Any]]:
        """Get a single record by ID."""
        try:
            result = await self._make_request("GET", f"{table}?id=eq.{record_id}")
            return result[0] if result else None
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get record: {str(e)}")
    
    async def get_multi(
        self, 
        table: str, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Get multiple records with pagination and optional filters."""
        try:
            params = {
                "order": "id",
                "offset": skip,
                "limit": limit
            }
            
            if filters:
                for key, value in filters.items():
                    params[key] = f"eq.{value}"
            
            result = await self._make_request("GET", table, params=params)
            return result or []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get records: {str(e)}")
    
    async def create(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record."""
        try:
            result = await self._make_request("POST", table, data=data)
            return result[0] if result else {}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create record: {str(e)}")
    
    async def update(self, table: str, record_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record by ID."""
        try:
            result = await self._make_request("PATCH", f"{table}?id=eq.{record_id}", data=data)
            return result[0] if result else {}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to update record: {str(e)}")
    
    async def delete(self, table: str, record_id: int) -> bool:
        """Delete a record by ID."""
        try:
            await self._make_request("DELETE", f"{table}?id=eq.{record_id}")
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete record: {str(e)}")
    
    async def search(
        self, 
        table: str, 
        search_params: Dict[str, Any],
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Search records with custom parameters."""
        try:
            params = {
                "order": "id",
                "offset": skip,
                "limit": limit
            }
            
            for key, value in search_params.items():
                params[key] = f"eq.{value}"
            
            result = await self._make_request("GET", table, params=params)
            return result or []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to search records: {str(e)}")


# Create global instance
supabase_service = SupabaseService()
