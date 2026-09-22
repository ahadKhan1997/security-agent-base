"""import asyncio
import httpx
from pydantic import BaseModel, HttpUrl
from config import settings

# Defines what valid data looks like
class TodoModel(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool

async def fetch_data(client: httpx.AsyncClient, todo_id: int):
    url = f"https://typicode.com{todo_id}"
    response = await client.get(url)

    # Strictly validates the incoming API data against our Pydantic model
    data = TodoModel(**response.json())
    print(f"Validated Todo {data.id}: {data.title} (Secret Key Loaded: {settings.api_key[:5]}...)")

async def main():
    # Capped concurrency using a Semaphore
    sem = asyncio.Semaphore(2) 
    
    async with sem:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # Runs both requests concurrently
            await asyncio.gather(
                fetch_data(client, 1),
                fetch_data(client, 2)
            )

if __name__ == "__main__":
    asyncio.run(main())"""

import asyncio
from pydantic import BaseModel
from config import settings

# This schema forces strict structural validation on data payloads
class TodoModel(BaseModel):
    userId: int
    id: int
    title: str
    completed: bool

# Simulated local secure database data bypassing the Eir network block
MOCK_API_DATABASE = {
    1: {"userId": 1, "id": 1, "title": "Delectus aut autem (Eir Hotspot Safe-Mock)", "completed": False},
    2: {"userId": 1, "id": 2, "title": "Quis ut nam facilis et officia qui (Eir Hotspot Safe-Mock)", "completed": False}
}

async def fetch_data(item_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        # Simulate network latency using standard asyncio sleep window
        await asyncio.sleep(0.4)
        
        raw_payload = MOCK_API_DATABASE.get(item_id)
        
        if raw_payload:
            # Strictly validates the payload structure against our Pydantic model
            data = TodoModel(**raw_payload)
            print(f"✅ Success | Item ID: {data.id} | Validated Title: '{data.title}'")
        else:
            print(f"❌ Error: Data not found for ID {item_id}")

async def main():
    # Defensive programming: Cap concurrency to 2 simultaneous operations
    sem = asyncio.Semaphore(2)
    
    print(f"🔒 App Security Initialized Natively. Active Key Signature: {settings.api_key[:7]}...")
    
    # Fires off both simulation tasks concurrently across the event loop
    await asyncio.gather(
        fetch_data(1, sem),
        fetch_data(2, sem)
    )

if __name__ == "__main__":
    asyncio.run(main())
