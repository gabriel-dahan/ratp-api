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

from difflib import SequenceMatcher

def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

class RATPAPI:
    
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
        
        self.categ = [
            'train',
            'metro',
            'bus',
            'tramway',
        ]

        self.lines = {
            '1': 'C01371',
            '2': 'C01372',
            '3': 'C01373',
            '3B': 'C01386',
            '4': 'C01374',
            '5': 'C01375',
            '6': 'C01376',
            '7': 'C01377',
            '7B': 'C01387',
            '8': 'C01378',
            '9': 'C01379',
            '10': 'C01380',
            '11': 'C01381',
            '12': 'C01382',
            '13': 'C01383',
            '14': 'C01384',
            'CDGVAL': 'C00563',
            'ORLYVAL': 'C01388',
            'FUN': 'C01385'
        }
    
    def __get_url(self, endpoint: str, lineid: str, params: dict) -> str:
        return self.base.format(lineid, endpoint, urlencode(params))

    def __get_formatted_time(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')
    
    def get_schedules(self, line: str, station_id: str = None, it: bool = True, complete: bool = False) -> dict:
        params = {
            'it': it,
            'complete': complete,
            'date': self.__get_formatted_time()
        }
        if station_id:
            res = requests.get(self.__get_url(f'stops/stop_area:IDFM:{station_id}/schedules', self.lines[line], params))
        else:
            res = requests.get(self.__get_url('schedules', self.lines[line], params))
        return res.json()
    
    def get_station_id(self, line: str, station: str) -> str | None:
        stations = self.get_stations(line)
        for el in stations:
            if similarity(el['name'], station) > 0.7:
                return el['id'].split(':')[-1]
        return None

    def get_stations(self, line: str, stop_points: bool = False, routes: bool = False) -> dict:
        params = {
            'stopPoints': stop_points,
            'routes' : routes
        }
        res = requests.get(self.__get_url('stops', self.lines[line], params))
        return res.json()
    
    def init_stations(self):
        url = "https://data.iledefrance-mobilites.fr/explore/dataset/referentiel-des-lignes/download/?format=json&timezone=Europe/Berlin&lang=fr"

        res = requests.get(url).text

        parsed_data = json.loads(res)

        train_lines = {}
        bus_lines = {}
        metro_lines = {}
        tramway_lines = {}
        conversion_table = { "metro": {}, "tramway": {}, "bus": {}, "train": {}}
        conv = {"metro": "metro", "tram": "tramway", "funicular": "metro", "bus": "bus", "rail": "train"}

        for entry in parsed_data:
            fields = entry.get("fields", {})
            name_line = fields.get("name_line")
            id_line = fields.get("id_line")
            transport_mode = fields.get("transportmode")
            line_data = {
                "shortname_groupoflines": fields.get("shortname_groupoflines"),
                "name_line": name_line,
                "operatorname": fields.get("operatorname"),
                "networkname": fields.get("networkname")
            }
            conversion_table[conv[transport_mode]][name_line] = id_line
            if conv[transport_mode] == "train":
                train_lines[id_line] = line_data
            elif conv[transport_mode] == "bus":
                bus_lines[id_line] = line_data
            elif conv[transport_mode] == "metro":
                metro_lines[id_line] = line_data
            elif conv[transport_mode] == "tramway":
                tramway_lines[id_line] = line_data

        with open("train_lines.json", "w") as f:
            json.dump(train_lines, f, indent=2)

        with open("bus_lines.json", "w") as f:
            json.dump(bus_lines, f, indent=2)

        with open("metro_lines.json", "w") as f:
            json.dump(metro_lines, f, indent=2)

        with open("tramway_lines.json", "w") as f:
            json.dump(tramway_lines, f, indent=2)
        with open("conversion_table.json", "w") as f:
            json.dump(conversion_table, f, indent=2)

    def get_real_time(self, line: str, station_id: str):
        return requests.get('https://api-iv.iledefrance-mobilites.fr/lines/line:IDFM:C01374/stops/stop_area:IDFM:71264/schedules?date=2024-04-07&it=true').json()


if __name__ == '__main__':
    rapi = RATPAPI().init_stations()
