import requests
import datetime
import xml.etree.ElementTree as ET
from dateutil.relativedelta import relativedelta
import pandas as pd 
import pathlib

ENDPOINT = "https://ssl.orpak.com/api40/TrackTecPublic/PublicService.asmx/ExecuteCommand"

cur_date = datetime.datetime.now().date()
start_date = cur_date -relativedelta(years=1) 

params = """
          <Paramaters>
          <ClientID>0d8eee08-8c34-438f-95dc-2fa901191dd4</ClientID>
          <CommandName>GetEventsHistory</CommandName>
          <ResultType>DEFAULT</ResultType>
          <DeviceIDs>81B16GBD5D00251</DeviceIDs>
          <SourceIDs>9,10,11,12,49,48,52</SourceIDs>
          <StartDate>2018/02/15 00:00:00</StartDate>
          <EndDate>2018/02/16 00:00:00</EndDate>
          <PageIndex>1</PageIndex>
          <PageSize>10000</PageSize>
          </Paramaters>
         """
r = requests.get(ENDPOINT + "?CommandData=" + params)


def querylist_builder():
    ret = [] # make an empty list to start throwing stuff onto
    q_start_date = start_date
    while q_start_date < cur_date:
        query_date = q_start_date.strftime("%Y/%m/%d") + " 00:00:00"
        end_date = (q_start_date + relativedelta(days=1)).strftime("%Y/%m/%d") + " 00:00:00"
        ret.append(params.format(query_date, end_date))
        q_start_date += relativedelta(days=1)
    return ret

def extract():
    queries = querylist_builder()

    pathlib.Path('/tmp/street_data').mkdir(parents=True, exist_ok=True) 
    for i,q in enumerate(queries):
        print("running extract query")
        url = ENDPOINT + "?CommandData=" + q
        print(url)
        r = requests.get(url)
        text_file = open("/tmp/street_data/" + str(i) + ".xml", 'w')
        data = r.text
        print(data)
        text_file.write(data)   
        print("data saved for {}".format(str(i)))
        text_file.close()
def parse():
    pass 

if '__name__' == '__main__':
    print('Running Script')
