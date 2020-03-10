"""Example usage of pystibmvib."""
import asyncio

import aiohttp

from pystibmvib import STIBAPIClient
from pystibmvib.STIBService import STIBService

CLIENT_ID = 'Wirff1HT1tTH7mLX1dMQAbOEHDoa' # Put your openapi client ID here
CLIENT_SECRET = 'tYKqSKbmjw3hKsoNtaaKKtXXP0sa' # Put your openapi client secret here


async def go(LOOP):
    stop_name = "scherdemael"
    lines_filter = [(46, "Glibert")]
    custom_session = aiohttp.ClientSession()

    APIClient = STIBAPIClient(LOOP, custom_session, CLIENT_ID, CLIENT_SECRET)

    service = STIBService(APIClient)
    print(await service.get_passages(stop_name, lines_filter))

    await custom_session.close()


if __name__ == '__main__':
    LOOP = asyncio.get_event_loop()
    LOOP.run_until_complete(go(LOOP))



