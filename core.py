import requests
from datetime import datetime

class RATPAPI:
    
    def __init__(self) -> None:
        self.base_api = 'https://api-iv.iledefrance-mobilites.fr/lines/line:IDFM:{0}/schedules?it=true&&complete={1}&date={2}'
        self.base_stations = 'https://api-iv.iledefrance-mobilites.fr/lines/line:IDFM:{0}/stops?stopPoints=false&routes=false'
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
    
    def __get_formatted_time(self) -> str:
        return datetime.now().strftime('%Y-%m-%d')
    
    def get_line_info(self, line: str, complete: bool = False) -> dict:
        res = requests.get(
            self.base_api.format(
                self.lines[line], 
                str(complete).lower(),
                self.__get_formatted_time()
            )
        )
        return res.json()
    
    def get_stations(self, line: str) -> dict:
        res = requests.get(
            self.base_stations.format(
                self.lines[line]
            )
        )
        return res.json()
    
if __name__ == '__main__':
    rapi = RATPAPI()
    print(rapi.get_line_info('1'))
    print('\n------------\n')
    print(rapi.get_stations('FUN'))