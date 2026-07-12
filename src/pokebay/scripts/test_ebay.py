# scripts/test_ebay.py
import asyncio
from pokebay.clients.ebay import search_listings

async def main():
    results = await search_listings("Charizard VMAX", limit=5)
    
    for item in results:
        print(item)
        print("---")

asyncio.run(main())
