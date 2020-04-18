"""Example usage of pystibmvib."""
import asyncio
import datetime
import json
import unittest

import aiohttp

from pystibmvib import STIBService, Passage, LineInfo
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
            self.assertEqual(passages[0]["message"], "foofr")
            self.assertEqual(passages[1]["message"], "")

            await custom_session.close()

        self.LOOP.run_until_complete(go(self.LOOP))

    def test_serializable(self):
        async def go(LOOP):
            stop_name = "scherdemael"
            lines_filter = [(46, "Glibert")]
            custom_session = aiohttp.ClientSession()

            APIClient = MockAPIClient()

            service = STIBService(APIClient)
            passages = await service.get_passages(stop_name, lines_filter)

            print(json.dumps(passages))

            await custom_session.close()

        self.LOOP.run_until_complete(go(self.LOOP))

    def test_atomic_passage_serialization(self):
        now = datetime.datetime.now()
        delta1 = datetime.timedelta(minutes=3, seconds=25)
        p = Passage(stop_id=42, lineId=21, destination="FooDest",
                    expectedArrivalTime=(now + delta1).strftime("%Y-%m-%dT%H:%M:%S"),
                    lineInfos=LineInfo(line_nr=21, line_type="B", line_color="#ffffff"), message="FooMsg", now=now)

        js = json.loads(json.dumps(p))
        self.assertEqual(js["stop_id"], 42)
        self.assertEqual(js["line_id"], 21)
        self.assertEqual(js["destination"], "FooDest")
        self.assertEqual(js["expected_arrival_time"], (now + delta1).strftime("%Y-%m-%dT%H:%M:%S"))
        self.assertEqual(js["line_color"], "#ffffff")
        self.assertEqual(js["line_type"], "B")
        self.assertEqual(js["message"], "FooMsg")
        self.assertEqual(js["arriving_in"]["min"], 3)
        self.assertEqual(js["arriving_in"]["sec"], 24)


if __name__ == '__main__':
    unittest.main()
