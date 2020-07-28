from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3


engine = create_engine('sqlite:///roboinvest.db')
Base = declarative_base()
conn = sqlite3.connect('roboinvest.db')
c = conn.cursor()

now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
timestamp = datetime.now()
email = 'email@email.com'
name = 'Smith, Robert'
routing = '123456789'
b_account = 'XXXXXXX'

datalist = [now, timestamp, email, routing, b_account]

class SL_Table(Base):
    """Create the table for the database."""

    __tablename__ = 'Client_Info'
    Primary = Column(Date, primary_key=True)
    Timestamp = Column(String)
    Email = Column(String)
    Routing = Column(String)
    Bank = Column(String)

class Table_Bind():
    SL_Table.__table__.create(bind=engine, checkfirst=True)


class DB_Entry:
    def db_entry():
         c.execute('CREATE TABLE IF NOT EXISTS `Client_Info`\
             (Primary_Key TEXT PRIMARY KEY, Timestamp TEXT, Email TEXT, Routing TEXT, Bank TEXT)')

         c.execute('INSERT INTO `Client_Info` VALUES(?, ?, ?, ?, ?)', datalist)
         conn.commit()
         c.close()

if __name__ == "__main__":
    DB_Entry.db_entry()
