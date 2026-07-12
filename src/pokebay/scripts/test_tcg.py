import asyncio
from pokebay.clients.tcgplayer import search_card_price

async def main():
    results = await search_card_price("Charizard VMAX")
    for card in results:
        print(card)
        print("---")

asyncio.run(main())
