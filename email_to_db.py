from datetime import datetime
from sqlalchemy import Column, Date, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3


engine = create_engine('sqlite:///stocks.db')
Base = declarative_base()
conn = sqlite3.connect('email_info.db')
c = conn.cursor()

now = str(datetime.now()).replace(':', '-').replace(' ', '-').replace('.', '-')
email = 'example@gmail.com'
email_text = 'Hello World.'

datalist = [now, email, email_text]

class SL_Table(Base):
    """Create the table for the database."""

    __tablename__ = 'Email_Info'
    Primary = Column(Date, primary_key=True)
    Email_Address = Column(String)
    Email_Text = Column(String)


class Table_Bind():
    SL_Table.__table__.create(bind=engine, checkfirst=True)


class DB_Entry:
    def db_entry():
         c.execute('CREATE TABLE IF NOT EXISTS `Email_Info`\
             (Primary_Key TEXT PRIMARY KEY, Email_Address TEXT, Email_Text TEXT)')

         c.execute('INSERT INTO `Email_Info` VALUES(?, ?, ?)', datalist)
         conn.commit()
         c.close()

if __name__ == "__main__":
    DB_Entry.db_entry()
