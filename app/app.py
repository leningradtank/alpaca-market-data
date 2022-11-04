from google.cloud import storage
import os
import datetime as dt
import pandas as pd
from alpaca_trade_api.rest import REST, TimeFrame

API_KEY = ''
SECRET_KEY = ''

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'servicekey_googlecloud.json'

class snpdata:
    
    def upload_to_bucket(bucket_name = 'alpaca-data', exchange = "IEX", symbol = "SPY"):
        bucket = storage.Client().bucket(bucket_name)
        yesterday = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)
        
        date_run = yesterday

        base_dst = "datatype=exchange={exchange}/symbol={symbol}/year={year}/month={month}/day={day}/{name}.csv"
#         date_run = dt.datetime.strptime(
#                 f"{date_run}T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
        dst = base_dst.format(
        date = date_run,
        exchange = exchange,
        symbol = symbol,
        year= date_run.year,
        month=date_run.month,
        day=date_run.day,
        name=f"{symbol}_{dt.datetime.strftime(date_run,'%Y-%m-%d')}"
    )
        local_path = 'snp_data.csv'
        blob = bucket.blob(dst)
        blob.upload_from_filename(local_path)
        print(bucket)
        os.remove("snp_data.csv")
        print("File removed locally")
        
    def get_yesterday_market_data( API_KEY, SECRET_KEY, market="SPY", timeframe=TimeFrame.Minute, extended_hours=False, exchange="IEX", write=False, path=None):

        yesterday = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=1)

        yesterday_market_open = yesterday.replace(hour=9, minute=30, second=0, microsecond=0).isoformat()
        yesterday_market_close = yesterday.replace(hour=16, minute=0, second=0, microsecond=0).isoformat()

        alpaca_rest_client = REST(API_KEY, SECRET_KEY)

        data = alpaca_rest_client.get_bars(market, TimeFrame.Minute, yesterday_market_open, yesterday_market_close).df    

        if write:
            if path is None:
                  print("IllegalArgument: Path cannot be None if write is True")

            data.to_csv(path)
            snpdata.upload_to_bucket()


        return print(data)

# snp = snpdata(API_KEY, SECRET_KEY)
snpdata.get_yesterday_market_data(API_KEY, SECRET_KEY, write=True, path="./snp_data.csv")

