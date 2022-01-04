from pyanimeclick import AnimeClick
import asyncio

ac = AnimeClick()

async def main():
    data = await ac.get_anime(480)
    print(data.title, data.year)
    print(data.average_duration)

asyncio.run(main())