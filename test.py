from pyanimeclick import AnimeClick

import asyncio

animeclick = AnimeClick()

async def main():
    data = await animeclick.search("Attack on Titan")

asyncio.run(main())