import requests
import shelve

searches = [{"query":"minilogue xd","price_max":"450","price_min":"200"},
            {"query":"norns","price_min":"400","price_max":"1100","currency":"USD"},
            {"query":"organelle m"}]
reverb_token = '<INSERT REVERB AUTH TOKEN>'
headers = {"Content-Type":"application/hal+json",
           "Accept":"application/hal+json",
           "Accept-Version":"3.0",
           "Authorization": "Bearer %s" % reverb_token}
endpoint = 'https://api.reverb.com/api/listings'


def notify(x):
    print (x['id'] ,x['title'], x['shop_name'], x['price']['amount'], x['_links']['web']['href'])


response_list = []
for query in searches:
    r = requests.get(endpoint, headers=headers, params=query)
    response = r.json()
    for item in response['listings']:
        response_list.append(item)

    pages = response['total_pages']

    for page in range(2, pages + 1):
        r = requests.get(endpoint, headers=headers, params=query)
        response = r.json()
        for item in response['listings']:
            response_list.append(item)

with shelve.open("reverb_db") as db:
    for item in response_list:
        id = str(item['id'])
        try:
            seen = db[id]
        except:
            seen = False
        if not seen:
            notify(item)
            db[id] = (item['id'], item['title'], item['shop_name'], item['price']['amount'],
                      item['_links']['web']['href'])