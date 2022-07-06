FROM python

RUN pip install wheel
RUN pip install pandas
RUN pip install google-api-python-client google-cloud google-cloud-bigquery google-cloud-storage 
RUN pip install alpaca_trade_api
RUN pip install datetime

# RUN pip os 
# RUN pip sys 

ENV GOOGLE_APPLICATION_CREDENTIALS "./key.json"

ADD app /app


WORKDIR /app

CMD python ./test.py '2022-02-13'