import http.client
from reference import appid, token
import json
from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
from threading import Timer

import reference

x = datetime.today()
y = x.replace(day = x.day + 1, hour = 18, minute = 45, second = 0, microsecond = 0)
delta_t = y - x

secs = delta_t.seconds+1

class Financial_Data:

    def ft_query():
        engine = create_engine('sqlite:///roboinvest.db')
        Base = declarative_base()
        conn_sql = sqlite3.connect(reference.database)
        # conn_sql = sqlite3.connect('roboinvest.db')
        c = conn_sql.cursor()

      	c.execute(
        	'SELECT \
         		count \
        	FROM \
            	price_history \
        	Where count = (select max(count) from price_history)')
      	
      	# Get count from price history table and increment it by one
 		mcount = []
		mcount = c.fetchall()
		mcount = mcount[0][0] + 1

        # now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
        # timestamp = datetime.now()
        conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
        headers = {
                'appid': appid,
                'token': token
                }

        for sec in reference.sec_list:

            # sec_data = []

            # Get data from vendor
            conn.request("GET", "/v1/data/" + sec + "/range?d=12%F12%F2099&adj=&olhv=0", headers=headers)
            res = conn.getresponse()
            data = res.read()
            dic = json.loads(data)
            for ix in range(len(dic['datarange'])):

            	# Create list for data entry into price history table.
				list_col = []
				list_col.append(dic['datarange'][ix]['date']['strdate'])
				list_col.append(sec)
				list_col.append(dic['datarange'][ix]['price'])
				list_col.append(mcount)
				list_col.append(datetime.now())

                try:
                	c.execute('INSERT INTO ' + table_name + ' VALUES(?, ?, ?, ?, ?)', list_col)
                    conn_sql.commit()
                except:
                    pass
        c.close()

t = Timer(secs, Financial_Data.ft_query, args=())
t.start()
