import requests
from datetime import datetime
from collections import namedtuple

try:
    # Python 3
    from urllib.parse import urlunparse, urlencode
except ImportError:
    # Python 2
    print('Try upgrading to Python3.')
    exit(1)

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
    
    def get_line_info(self, line: str, it: bool = True, complete: bool = False) -> dict:
        params = {
            'it': it,
            'complete': complete,
            'date': self.__get_formatted_time()
        }
        res = requests.get(self.__get_url('schedules', self.lines[line], params))
        return res.json()
    
    def get_stations(self, line: str, stop_points: bool = False, routes: bool = False) -> dict:
        params = {
            'stopPoints': stop_points,
            'routes' : routes
        }
        res = requests.get(self.__get_url('stops', self.lines[line], params))
        return res.json()
    
if __name__ == '__main__':
    rapi = RATPAPI()
    print(rapi.get_line_info('1'))
    print('\n------------\n')
    print(rapi.get_stations('FUN'))