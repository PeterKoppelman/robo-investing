import http.client
from auth import appid, token
import json
from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3


engine = create_engine('sqlite:///roboinvest.db')
Base = declarative_base()
conn_sql = sqlite3.connect('roboinvest.db')
c = conn_sql.cursor()
now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
timestamp = datetime.now()

class Financial_Data:
    def ft_query():
        account_bal = 5000
        conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
        headers = {
                'appid': appid,
                'token': token
                }
        sec_list = ["VOO", "PRULX", "VTIAX", "PFORX"]

        for sec in sec_list:

            sec_data = []
            conn.request("GET", "/v1/data/" + sec + "/range?start=1%2F1%2F2000&adj=&olhv=0", headers=headers)
            res = conn.getresponse()
            data = res.read()
            dic = json.loads(data)
            for ix in range(len(dic['datarange'])):
                list_col = []
                list_col = [datetime.strptime(dic['datarange'][ix]['date']['strdate'], '%m/%d/%Y'), dic['datarange'][ix]['price']]

                c.execute('CREATE TABLE IF NOT EXISTS ' + sec + '\
                (Datetime DATE PRIMARY KEY, Price NUMERIC)')

                try:
                    c.execute('INSERT INTO ' + sec + ' VALUES(?, ?)', list_col)
                    conn_sql.commit()
                except:
                    pass
        c.close()

if __name__ == "__main__":
    Financial_Data.ft_query()
