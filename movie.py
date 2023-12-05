import pandas as pd
import json
import requests



def get_movie(start, end):
    # start_date = 
    r = requests.get('https://boxoffice.tfi.org.tw/api/export?start=2023/11/13&end=2023/11/19')
    data= json.loads(r.text)

    # # Extract the 'list' key which contains movie information
    movies_list = data['list']

    # # Convert the list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(movies_list)
    # # df = pd.read_html('https://boxoffice.tfi.org.tw/api/export?start=2023/11/13&end=2023/11/19')

    df['start'] = pd.to_datetime(data['start'])
    df['end'] = pd.to_datetime(data['end'])

