from datetime import date
java = 1589401579221/1000.0

data = {
    '1' : {
        'name' : 'shakeel',
        'msg' : 'i am shakeel'
    },
    '2' : {
        'name' : 'usman',
        'msg' : 'i am usman'
    },
    '3' : {
        'name' : 'shakeel',
        'msg' : 'my another message'
    },
    '4' : {
        'name' : 'usman',
        'msg' : 'this is another msg'
    }
}


users = dict()

for k,v in data.items():
    if v['name'] not in users:
        users[v['name']] = { k : v}
    else:
        users[v['name']].update({k : v})

print(date.fromtimestamp(java).
