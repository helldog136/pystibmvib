"""Example usage of pystibmvib."""
import asyncio
import datetime
import unittest

import aiohttp

from pystibmvib import STIBService
from tests.pystibmvib import MockAPIClient


class TestPassages(unittest.TestCase):
    def setUp(self):
        self.LOOP = asyncio.get_event_loop()

    def tearDown(self):
        self.LOOP.close()

    def test_filtered_out(self):
        async def go(LOOP):
            stop_name = "scherdemael"
            lines_filter = [(46, "Glibert")]
            custom_session = aiohttp.ClientSession()

            APIClient = MockAPIClient()

            service = STIBService(APIClient)
            passages = await service.get_passages(stop_name, lines_filter)

            now = datetime.datetime.now()
            delta1 = datetime.timedelta(minutes=3, seconds=25)
            delta2 = datetime.timedelta(minutes=13, seconds=22)

            # Check message
            self.assertEqual(passages[0].message, "foofr")
            self.assertEqual(passages[1].message, "")

            await custom_session.close()

        self.LOOP.run_until_complete(go(self.LOOP))


if __name__ == '__main__':
    unittest.main()
