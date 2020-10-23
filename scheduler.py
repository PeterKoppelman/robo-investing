'''this is the scheduler program for the roboinvest system
Peter Koppelman September 30, 2020'''

import http.client
import json
import sqlite3
import sys
from datetime import datetime
from datetime import date
from reference import appid, token

import reference


def scheduler():
    # only run this Monday - Friday. 0 = Monday, 4 = Friday
    dow = datetime.today().weekday()
    if dow > 4:
        print("It's the weekend - scheduluer does not run")
        sys.exit("It's the weekend - scheduluer does not run")
        return

    try:
        connect = sqlite3.connect(reference.database)
        cursor = connect.cursor()
    except sqlite3.OperationalError:
        print('There was a problem opening up the roboinvest database')
        sys.exit('There was a problem opening up the roboinvest database')
        return

    headers = {
        'appid': reference.appid,
        'token': reference.token
    }

    for sec in reference.sec_list:
        cursor.execute(
            'SELECT \
                sec, \
                count, \
                As_of_Date \
            FROM \
                price_history \
            Where count = (select max(count) from price_history where Sec = ?) and \
                Sec = ?', (sec, sec))

        # Get count from price history table and increment it by one
        minfo = cursor.fetchall()
        mcount = minfo[0][1] + 1
        most_recent_date = minfo[0][2]
 
        # Get data from vendor
        try:
            conn_ft = http.client.HTTPSConnection("ftl.fasttrack.net")
            conn_ft.request("GET",
                "/v1/data/" + sec + "/range?d=2099-12-31", headers=headers)
        except:
            print('Could not connect to the vendor database')
            sys.exit('Could not connec to the vendor database')
            return

        res = conn_ft.getresponse()
        data = res.read()
        dic = json.loads(data)

        for i, j in enumerate(dic['datarange']):
            # if the most recent date in the database is the same as the date that we got from
            # the vendor, we're getting data that we already have. This may be due to the vendor
            # not updating data or that the current date is a holiday.
            # Peter Koppelman Sept 29, 2020
            if j.get('date').get('strdate') == most_recent_date:
                print('Close data has the same date as the most recent information for '+sec+
                    ' in the price history table')
                continue

			# Create list for data entry into price history table.
            list_col = []
            list_col.append(j.get('date').get('strdate'))
            list_col.append(sec)
            list_col.append(j.get('price'))
            list_col.append(mcount)
            list_col.append(datetime.now())

            cursor.execute('INSERT INTO price_history VALUES(?, ?, ?, ?, ?)', list_col)
            connect.commit()
    cursor.close()

if __name__ == "__main__":
    scheduler()
