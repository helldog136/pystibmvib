import asyncio
import unittest

from pystibmvib.ShapefileService import ShapefileService
from tests.pystibmvib import MockAPIClient


class TestShapefileReader(unittest.TestCase):
    def setUp(self):
        self.LOOP = asyncio.get_event_loop()

    def tearDown(self):
        self.LOOP.close()

    def test_filtered_out(self):
        async def go(LOOP):
            APIClient = MockAPIClient()

            sf_reader = ShapefileService(APIClient)

            frinfo = await sf_reader.get_stop_infos("Scherdemael")
            nlinfo = await sf_reader.get_stop_infos("Scherdemaal")


            self.assertEqual(frinfo.get_line_info(46).get_line_color(), nlinfo.get_line_info(46).get_line_color())
            self.assertEqual(frinfo.get_line_info(46).get_line_type(), nlinfo.get_line_info(46).get_line_type())
            self.assertEqual(frinfo.get_line_info(46).get_line_nr(), nlinfo.get_line_info(46).get_line_nr())


            self.assertEqual(frinfo.get_line_info(46).get_line_color(), "#DE3B21")
            self.assertEqual(frinfo.get_line_info(46).get_line_type(), "B")
            self.assertEqual(frinfo.get_line_info(46).get_line_nr(), 46)

        self.LOOP.run_until_complete(go(self.LOOP))

if __name__ == '__main__':
    unittest.main()
