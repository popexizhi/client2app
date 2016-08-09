import requests

res = requests.post('http://192.168.1.99:8888/api/add_message/1234', json={"mytext":"lalala"})
if res.ok:
    print res.status_code()
