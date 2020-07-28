import sqlite3
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlite3

engine = create_engine('sqlite:///roboinvest.db')
Base = declarative_base()
conn_sql = sqlite3.connect('roboinvest.db')
c = conn_sql.cursor()


class Query_Database:
    def get_posts():
        sec_list = sec_list = ['VOO', 'PRULX', 'VTIAX', 'PFORX', 'FDHY']
        sec_latest_vals = []
        for sec in sec_list:
            c.execute('SELECT * FROM ' + sec + ' ORDER BY Datetime DESC LIMIT 1')
            sec_latest_vals.append(c.fetchall())
        print(sec_latest_vals)
        return sec_latest_vals

if __name__ == '__main__':
