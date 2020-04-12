import json
import logging
from datetime import *

from pystibmvib.service.ShapefileService import ShapefileService
from pystibmvib.client import AbstractSTIBAPIClient
from pystibmvib.domain.passages import Passage

LOGGER = logging.getLogger(__name__)

PASSING_TIME_BY_POINT_SUFFIX = "/OperationMonitoring/4.0/PassingTimeByPoint/"


class STIBService:
    def __init__(self, stib_api_client: AbstractSTIBAPIClient):
        self._shapefile_service = ShapefileService(stib_api_client)
        self.api_client = stib_api_client

    async def get_passages(self, stop_name, line_filters=None, max_passages=15, lang: str = 'fr', now=datetime.now()):
        stop_infos = await self._shapefile_service.get_stop_infos(stop_name)

        atomic_stop_infos = stop_infos.get_lines()
        if line_filters is not None and len(line_filters) > 0:
            line_filter_nr = [k[0] for k in line_filters]
            line_filter_dest = [k[1].upper() for k in line_filters]
            atomic_stop_infos = filter(
                (lambda s: s.get_line_nr() in line_filter_nr and s.get_destination().upper() == line_filter_dest[line_filter_nr.index(s.get_line_nr())]),
                atomic_stop_infos)
        passages = []
        for atomic in atomic_stop_infos:
            call_url_suffix = PASSING_TIME_BY_POINT_SUFFIX + atomic.get_stop_id()

            raw_passages = await self.api_client.api_call(call_url_suffix)
            raw_passages = json.loads(raw_passages)
            for point in raw_passages["points"]:
                for json_passage in point["passingTimes"]:
                    if len(passages) >= max_passages:
                        break
                    message = ""
                    try:
                        message = json_passage["message"][lang]
                    except:
                        pass
                    passages.append(Passage(stop_id=point["pointId"],
                                            lineId=json_passage["lineId"],
                                            destination=json_passage["destination"][lang],
                                            expectedArrivalTime=json_passage["expectedArrivalTime"],
                                            lineInfos=await self._shapefile_service.get_line_info(
                                                json_passage["lineId"]),
                                            message=message,
                                            now=now))
        return passages
