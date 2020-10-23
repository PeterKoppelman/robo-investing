import http.client
import json
conn = http.client.HTTPSConnection("ftlightning.fasttrack.net")

conn.request("GET", "/v1/auth/login?account=300724&pass=1243OEIL&appid=F075C6E1-759C-4009-9B47-5FE284F31F55")

res = conn.getresponse()
data = json.loads(res.read())

appid = data['appid']
token = data['token']
print(data)
