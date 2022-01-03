from pyanimeclick import AnimeClick
import asyncio

ac = AnimeClick()

async def main():
    data = await ac.get_anime(480)
    print(data.title, data.thumb)

asyncio.run(main())