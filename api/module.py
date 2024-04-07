import requests
from datetime import datetime
from collections import namedtuple
import json

try:
    # Python 3
    from urllib.parse import urlunparse, urlencode
except ImportError:
    # Python 2
    print('Try upgrading to Python3.')
    exit(1)

class RATP_API:
    
    def __init__(self) -> None:

        self.components = namedtuple(
            typename = 'base_components',
            field_names = ['scheme', 'netloc', 'url', 'params', 'query', 'fragment']
        )

        self.base: str = urlunparse(
            self.components(
                scheme = 'https',
                netloc = 'api-iv.iledefrance-mobilites.fr',
                url = '/lines/line:IDFM:{0}/{1}',
                params = '',
                query = '{2}',
                fragment = ''
            )
        )

        self.base_times = 'https://api-iv.iledefrance-mobilites.fr/lines/v2/line:IDFM:{0}/stops/stop_area:IDFM:{1}/realTime'

        with open("./data/conversion_table.json", "r") as l:
            self.lines = json.load(l)

    def __get_url(self, endpoint: str, lineid: str, params: dict) -> str:
        return self.base.format(lineid, endpoint, urlencode(params))

    def __get_formatted_time(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')
    
    def get_schedules(self, line_id: str, station_id: str = None, it: bool = True, complete: bool = False) -> dict:
        params = {
            'it': it,
            'complete': complete,
            'date': self.__get_formatted_time()
        }
        if station_id:
            res = requests.get(self.__get_url(f'stops/stop_area:IDFM:{station_id}/schedules', line_id, params))
        else:
            res = requests.get(self.__get_url('schedules', line_id, params))
        return res.json()

    def get_stations(self, line_id: str, stop_points: bool = False, routes: bool = False) -> dict:
        params = {
            'stopPoints': stop_points,
            'routes' : routes
        }
        res = requests.get(self.__get_url('stops', line_id, params))
        return res.json()

    def get_real_time(self, line_id: str, station_id: str, it: bool = True):
        requests.get('https://api-iv.iledefrance-mobilites.fr/lines/line:IDFM:C01374/stops/stop_area:IDFM:71264/schedules?date=2024-04-07&it=true').json()
        params = {
            'date': self.__get_formatted_time(),
            'it': it
        }
        res = requests.get(self.__get_url(f'stops/stop_area:IDFM:{station_id}/schedules', line_id, params))
        return res.json()

if __name__ == '__main__':
    
    rapi = RATP_API()
    print(rapi.get_line_id('L'))
