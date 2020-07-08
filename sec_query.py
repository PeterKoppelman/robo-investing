import http.client
import json
from auth import appid, token

class Financial_Data:
    def ft_query():
        account_bal = 5000
        asset_allocation = [0.25, 0.1, 0.3, 0.1, 0.25]
        conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")
        headers = {
                'appid': appid,
                'token': token
                }
        sec_list = ["VOO", "PRULX", "VTIAX", "PFORX", "FDHY", "SPY"]

        sec_val_list = []
        for sec in sec_list:

            conn.request("GET", "/v1/data/" + sec + "/divadjprices", headers=headers)

            res = conn.getresponse()
            data = res.read()
            dic = json.loads(data)
            sec_val_list.append(dic["prices"][-1])

        dom_stock  = int((account_bal * asset_allocation[0]) / sec_val_list[0])
        dom_stock_rem = asset_allocation[0] * account_bal - (dom_stock * sec_val_list[0])
        gov_bond  = int((account_bal * asset_allocation[1]) / sec_val_list[1])
        gov_bond_rem = asset_allocation[1] * account_bal - (gov_bond * sec_val_list[1])
        int_stock  = int((account_bal * asset_allocation[2]) / sec_val_list[2])
        int_stock_rem = asset_allocation[2] * account_bal - (int_stock * sec_val_list[2])
        int_bond  = int((account_bal * asset_allocation[3]) / sec_val_list[3])
        int_bond_rem = asset_allocation[3] * account_bal - (int_bond * sec_val_list[3])
        corp_bond  = int(account_bal * asset_allocation[4] / sec_val_list[4])
        corp_bond_rem = asset_allocation[4] * account_bal - (corp_bond * sec_val_list[4])
        ttl_rem = dom_stock_rem + gov_bond_rem + int_stock_rem + int_bond_rem + corp_bond_rem
        rem_spy = ttl_rem / sec_val_list[5]

        print("Your portfolio consists of the following...")
        print("{} shares of {} at {}.".format(dom_stock, sec_list[0], sec_val_list[0]))
        print("{} shares of {} at {}.".format(gov_bond, sec_list[1], sec_val_list[1]))
        print("{} shares of {} at {}.".format(int_stock, sec_list[2], sec_val_list[2]))
        print("{} shares of {} at {}.".format(int_bond, sec_list[3], sec_val_list[3]))
        print("{} shares of {} at {}.".format(corp_bond, sec_list[4], sec_val_list[4]))
        print("{} shares of {} at {}.".format(round(rem_spy, 4), sec_list[5], sec_val_list[5]))

        return sec_val_list
        return dom_stock
        return dom_stock_rem
        return gov_bond
        return gov_bond_rem
        return int_stock
        return int_stock_rem
        return int_bond
        return int_bond_rem
        return corp_bond
        return corp_bond_rem
        return ttl_rem
        return rem_spy

if __name__ == "__main__":
    Financial_Data.ft_query()
